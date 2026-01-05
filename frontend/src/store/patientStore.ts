import { useAuthStore } from "@/Features/auth/store/useAuthStore";
import { PatientApiResponse } from "@/types/patientApityping";
import { create } from "zustand";

export type Status =
  | "Scheduled"
  | "Checked In"
  | "Pre-Procedure"
  | "In-Progress"
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
  // [key: string]: any;
}

interface PatientStore {
  patients: Patient[];
  selectedPatient: Patient | null;
  setPatients: (patients: Patient[]) => void;
  setSelectedPatient: (patient: Patient | null) => void;
  clearSelectedPatient: () => void;
  fetchPatients: () => Promise<void>;
  findPatientByPatientNumber: (patientNumber: string) => Promise<Patient>;
  updatePatientStatus: (
    patientNumber: string,
    newStatus: Status,
    notes?: string
  ) => Promise<{ success: boolean; message?: string }>;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const usePatientStore = create<PatientStore>((set, ) => ({
  patients: [],
  selectedPatient: null,

  setPatients: (patients) => set({ patients }),
  setSelectedPatient: (patient) => set({ selectedPatient: patient }),
  clearSelectedPatient: () => set({ selectedPatient: null }),

  // ✅ Fetch all patients
  fetchPatients: async () => {
    const token = useAuthStore.getState().token;

    try {
      const res = await fetch(`${API_BASE}/api/patients/list/`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error("Failed to fetch patients");
      const data = await res.json();

      // Normalize each patient record
      const normalized = data.map((p: PatientApiResponse) => ({
        patientNumber: p.code,
        firstName: p.first_name,
        lastName: p.last_name,
        contactEmail: p.email,
        phoneNumber: p.contact || "",
        streetAddress: p.address || "",
        city: p.district || "",
        state: p.state || "",
        country: p.country || "",
        status: p.current_status || "Scheduled",
        notes: p.notes || "",
      }));

      set({ patients: normalized });
    } catch (err) {
      console.error("Error fetching patients:", err);
      set({ patients: [] });
    }
  },

  // Existing search and update functions
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
    } catch (err: unknown) {
  console.error(err);

  return {
    success: false,
    message:
      err instanceof Error
        ? err.message
        : "Failed to update patient status",
  };
}

  },
}));
