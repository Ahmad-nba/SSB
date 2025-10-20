import { useAuthStore } from "@/Features/auth/store/useAuthStore";
import { create } from "zustand";

export type Status =
  | "Scheduled"
  | "Checked In"
  | "Pre-Procedure"
  | "In Progress"
  | "Closing"
  | "Recovery"
  | "Complete"
  | "Dismissal";

export interface Patient {
  patientNumber: string;
  firstName: string;
  lastName: string;
  contactEmail: string;
  phoneNumber: string;
  streetAddress: string;
  city: string;
  state: string;
  country: string;
  status: Status;
  notes?: string;
  [key: string]: any;
}

interface PatientStore {
  patients: Patient[];
  selectedPatient: Patient | null;
  setPatients: (patients: Patient[]) => void;
  setSelectedPatient: (patient: Patient | null) => void;
  clearSelectedPatient: () => void;
  findPatientByPatientNumber: (patientNumber: string) => Promise<Patient>;
  updatePatientStatus: (
    patientNumber: string,
    newStatus: Status,
    notes?: string
  ) => Promise<{ success: boolean; message?: string }>;
}

export const usePatientStore = create<PatientStore>((set, get) => ({
  patients: [],
  selectedPatient: null,

  setPatients: (patients) => set({ patients }),
  setSelectedPatient: (patient) => set({ selectedPatient: patient }),
  clearSelectedPatient: () => set({ selectedPatient: null }),

  findPatientByPatientNumber: async (patientNumber) => {
    const token = useAuthStore.getState().token;
    try {
      const res = await fetch(
        `http://localhost:8000/api/patients/search/?patientNumber=${patientNumber}`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!res.ok) throw new Error("Patient not found");

      const data = await res.json();

      // Normalize API response to match our store Patient interface
      const normalizedPatient: Patient = {
        patientNumber: data.code,
        firstName: data.first_name,
        lastName: data.last_name,
        contactEmail: data.email,
        phoneNumber: data.contact || "",
        streetAddress: data.address || "",
        city: data.district || "",
        state: data.state || "",
        country: data.country || "",
        status: data.current_status || "Scheduled",
        notes: data.notes || "",
      };

      set({ selectedPatient: normalizedPatient });
      return normalizedPatient;
    } catch (err) {
      console.error(err);
      set({ selectedPatient: null });
      throw err;
    }
  },

  updatePatientStatus: async (patientNumber, newStatus, notes = "") => {
    const token = useAuthStore.getState().token;
    try {
      const res = await fetch(
        `http://localhost:8000/api/patients/update-status/${patientNumber}/`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ current_status: newStatus, notes }),
        }
      );

      if (!res.ok) {
        const errData = await res.json();
        return {
          success: false,
          message: errData.detail || "Error updating status",
        };
      }

      const data = await res.json();

      // Normalize updated patient too
      const updatedPatient: Patient = {
        patientNumber: data.code,
        firstName: data.first_name,
        lastName: data.last_name,
        contactEmail: data.email,
        phoneNumber: data.contact || "",
        streetAddress: data.address || "",
        city: data.district || "",
        state: data.state || "",
        country: data.country || "",
        status: data.current_status || "Scheduled",
        notes: data.notes || "",
      };

      set((state) => ({
        selectedPatient: updatedPatient,
        patients: state.patients.map((p) =>
          p.patientNumber === updatedPatient.patientNumber
            ? updatedPatient
            : p
        ),
      }));

      return { success: true };
    } catch (err: any) {
      console.error(err);
      return { success: false, message: err.message };
    }
  },
}));
