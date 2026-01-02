'use client';
import React, { useState, useEffect } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import { LuUserPlus, LuClipboardPlus } from "react-icons/lu";
import { CiSearch } from "react-icons/ci";
import ProtectedRoute from "@/components/guards/withAuthRedirect";
import { IPatientFormInput, IPatients } from "@/types/patientStore";
import { useAuthStore } from "@/Features/auth/store/useAuthStore";

// Utility: generate unique 6-character alphanumeric patient code
const generatePatientId = () => {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  return Array.from({ length: 6 }, () =>
    chars.charAt(Math.floor(Math.random() * chars.length))
  ).join("");
};

const PatientInformation = () => {
  const [patients, setPatients] = useState<IPatients[]>([]);
  const [_searchInput, setSearchInput] = useState("");
  const [_searchResults, setSearchResults] = useState<IPatients[]>([]);
  const [formMessage, setFormMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);
  const [loading, setLoading] = useState(false);
  const [doctors, setDoctors] = useState<
    { id: number; username: string; email: string }[]
  >([]);
  const token = useAuthStore.getState().token;

  // Hook Form setup
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<IPatientFormInput>({
    defaultValues: {
      firstName: "",
      lastName: "",
      streetAddress: "",
      city: "",
      state: "",
      country: "",
      phoneNumber: "",
      contactEmail: "",
      doctor_id: 0,
      roomNumber: "",
      custodianName: "",
      custodianPhone: "",
      custodianEmail: "",
    },
  });

  // Fetch doctors
  useEffect(() => {
    if (!token) return;
    fetch("http://localhost:8000/api/doctors/list/", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then(setDoctors)
      .catch((err) => console.error("Failed to load doctors:", err));
  }, [token]);

  // Fetch patients
  useEffect(() => {
    if (!token) return;
    (async () => {
      try {
        const res = await fetch("http://localhost:8000/api/patients/list/", {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });
        if (!res.ok) throw new Error("Failed to fetch patients");
        const data = await res.json();
        setPatients(data);
      } catch (err) {
        console.error(err);
      }
    })();
  }, [token]);

  // Add patient
  const addPatient = async (patient: IPatients) => {
    if (!token) {
      setFormMessage({
        type: "error",
        text: "You are not authorized. Please log in again.",
      });
      return;
    }
    setLoading(true);
    try {
      // Map camelCase -> snake_case for backend
      const payload = {
        first_name: patient.firstName,
        last_name: patient.lastName,
        patient_number: patient.patientNumber,
        address: patient.streetAddress,
        district: patient.state || "",
        contact: patient.phoneNumber,
        email: patient.contactEmail,
        doctor_id: patient.doctor_id,
        room_number: patient.roomNumber || "",
        custodian_name: patient.custodianName || "",
        custodian_phone: patient.custodianPhone || "",
        custodian_email: patient.custodianEmail || "",
        city: patient.city || "",
        country: patient.country || "",
        date_of_birth: patient.dateOfBirth || "",
      };
      const res = await fetch("http://localhost:8000/api/patients/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });
      // const dataR = await res.json();
      // console.log("Response:", dataR);
      // if (!res.ok) {
      //   throw new Error(`Failed: ${res.statusText} - ${JSON.stringify(dataR)}`);
      // }
      const data = await res.json();
      if (!res.ok) throw new Error(`Failed to add patient: ${data.detail || res.statusText}`);
      setPatients((prev) => [...prev, data.patient || patient]);
      setFormMessage({
        type: "success",
        text: `Patient ${data.patient?.code} added successfully`,
      });
      reset();
    } catch (err: any) {
      setFormMessage({
        type: "error",
        text: err.message || "Unexpected error occurred",
      });
    } finally {
      setLoading(false);
    }
  };

  // Form submit handler
  const onSubmit: SubmitHandler<IPatientFormInput> = (data) => {
    const newPatient: IPatients = {
      firstName: data.firstName,
      lastName: data.lastName,
      patientNumber: generatePatientId(),
      streetAddress: data.streetAddress,
      state: data.state,
      city: data.city,
      country: data.country,
      dateOfBirth: data.dateOfBirth,
      age: data.age,
      phoneNumber: data.phoneNumber,
      contactEmail: data.contactEmail,
      doctor_id: data.doctor_id || 0,
      roomNumber: data.roomNumber || "",
      custodianName: data.custodianName || "",
      custodianPhone: data.custodianPhone || "",
      custodianEmail: data.custodianEmail || "",
      status: "Checked In", // Required field in IPatients
    };
    addPatient(newPatient);
  };

  return (
    <ProtectedRoute>
      <div className="container mx-auto flex flex-col justify-center items-center lg:px-4 px-2 py-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <LuUserPlus className="size-5 lg:size-6 text-accentMain" />
            <h1 className="md:text-2xl font-bold text-viking-950">
              Patient Information Management
            </h1>
          </div>
          <button
            className="bg-viking-700 p-2 rounded-lg lg:hidden text-viking-50 shadow-md hover:bg-viking-800 transition-colors flex justify-center items-center"
            onClick={() => setSearchInput("")}
          >
            <CiSearch className="stroke-2" />
          </button>
        </div>
        <div className="lg:grid lg:grid-cols-2 lg:gap-8 md:flex md:flex-col md:items-center md:justify-center md:w-full">
          <main className="lg:col-span-1 rounded-lg p-3 lg:p-8 shadow-lg">
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-viking-900">
                Add New Patient
              </h2>
              <p className="text-viking-700 text-base">
                Enter patient information to start tracking their surgical progress.
              </p>
            </div>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
              {/* ✅ Feedback message */}
              {formMessage && (
                <div
                  className={`p-4 rounded-md ${
                    formMessage.type === "success"
                      ? "bg-green-100 text-green-800"
                      : "bg-red-100 text-red-800"
                  }`}
                >
                  {formMessage.text}
                </div>
              )}
              {/* 🧍‍♂️ Patient Info */}
              <div className="border border-gray-200 rounded-2xl p-6 shadow-sm space-y-6">
                <h3 className="text-xl font-semibold text-viking-900 mb-4">
                  Patient Information
                </h3>
                <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <InputField
                    id="firstName"
                    label="First Name"
                    register={register}
                    errors={errors}
                    required
                  />
                  <InputField
                    id="lastName"
                    label="Last Name"
                    register={register}
                    errors={errors}
                    required
                  />
                </section>
                <InputField
                  id="streetAddress"
                  label="Street Address"
                  register={register}
                  errors={errors}
                  required
                />
                <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  {["city", "state", "country"].map((field) => (
                    <InputField
                      key={field}
                      id={field}
                      label={field.charAt(0).toUpperCase() + field.slice(1)}
                      register={register}
                      errors={errors}
                    />
                  ))}
                </section>
                {/* 👶 Date of Birth + Age + Nationality */}
                <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  <div>
                    <label
                      htmlFor="dateOfBirth"
                      className="block text-sm font-medium text-gray-700 mb-1"
                    >
                      Date of Birth
                    </label>
                    <input
                      id="dateOfBirth"
                      type="date"
                      {...register("dateOfBirth", {
                        required: "Date of birth is required",
                      })}
                      className={`block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-accentMain focus:border-accentMain ${
                        errors.dateOfBirth ? "border-red-500" : ""
                      }`}
                    />
                    {errors.dateOfBirth && (
                      <p className="text-red-600 text-sm mt-1">
                        {errors.dateOfBirth.message}
                      </p>
                    )}
                  </div>
                  <InputField
                    id="age"
                    label="Age"
                    type="number"
                    placeholder="Enter age"
                    register={register}
                    errors={errors}
                    required
                  />
                  <InputField
                    id="nationality"
                    label="Nationality"
                    placeholder="e.g. Ugandan"
                    register={register}
                    errors={errors}
                    required
                  />
                </section>
                <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <InputField
                    id="phoneNumber"
                    label="Phone Number"
                    placeholder="+256 700 000000"
                    register={register}
                    errors={errors}
                    required
                  />
                  <InputField
                    id="contactEmail"
                    label="Contact Email"
                    placeholder="email@example.com"
                    register={register}
                    errors={errors}
                    required
                  />
                </section>
              </div>
              {/* 👨‍👩‍👧 Custodian Info */}
              <div className="border border-gray-200 rounded-2xl p-6 shadow-sm space-y-6">
                <h3 className="text-lg font-semibold text-viking-900 mb-4">
                  Custodian Information
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  <InputField
                    id="custodianName"
                    label="Custodian Name"
                    register={register}
                    errors={errors}
                  />
                  <InputField
                    id="custodianPhone"
                    label="Custodian Phone"
                    register={register}
                    errors={errors}
                  />
                  <InputField
                    id="custodianEmail"
                    label="Custodian Email"
                    register={register}
                    errors={errors}
                  />
                </div>
              </div>
              {/* 🩺 Assign Doctor */}
              <div className="border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
                <h3 className="text-lg font-semibold text-viking-900 mb-4">
                  Assign Doctor
                </h3>
                <select
                  className="border border-gray-400 rounded-md px-4 py-2 w-full focus:ring-accentMain focus:border-accentMain"
                  {...register("doctor_id", {
                    required: "Please assign a doctor",
                  })}
                >
                  <option value="">Select Doctor</option>
                  {doctors.map((doc) => (
                    <option key={doc.id} value={doc.id}>
                      {doc.username} ({doc.email})
                    </option>
                  ))}
                </select>
                {errors.doctor_id && (
                  <p className="text-red-600 text-sm mt-1">
                    {errors.doctor_id.message}
                  </p>
                )}
              </div>
              {/* 🏥 Room Number */}
              <div className="border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
                <InputField
                  id="roomNumber"
                  label="Room Number"
                  placeholder="Room 12B"
                  register={register}
                  errors={errors}
                />
              </div>
              {/* 🧾 Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className={`bg-accentMain text-white py-3 rounded-md flex justify-center items-center gap-2 w-full font-semibold transition-colors ${
                  loading ? "opacity-50 cursor-not-allowed" : "hover:bg-viking-800"
                }`}
              >
                <LuClipboardPlus className="size-6" />
                <span>{loading ? "Adding..." : "Add Patient"}</span>
              </button>
            </form>
          </main>
        </div>
      </div>
    </ProtectedRoute>
  );
};

// Simple reusable input component
const InputField = ({
  id,
  label,
  register,
  errors,
  required,
  placeholder,
  type,
}: any) => (
  <div className="flex flex-col">
    <label htmlFor={id} className="block text-viking-800 mb-1">
      {label}
    </label>
    <input
      id={id}
      placeholder={placeholder}
      type={type}
      className="border border-gray-400 rounded-md px-4 py-1"
      {...register(
        id,
        required ? { required: `${label} is required` } : {}
      )}
    />
    {errors[id] && (
      <p className="text-red-600 text-sm mt-1">{errors[id]?.message}</p>
    )}
  </div>
);

export default PatientInformation;
