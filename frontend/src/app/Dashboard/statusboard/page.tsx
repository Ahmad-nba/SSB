"use client";
import { useEffect } from "react";
import { MdMonitor } from "react-icons/md";
import { LuUsers } from "react-icons/lu";
import { usePatientStore } from "@/store/patientStore";
import StatusCard from "@/Features/statusBoard/components/statusCard";
import ActivePatientCard from "@/Features/statusBoard/components/activePatientCard";

export default function StatusBoardPage() {
  const patients = usePatientStore((state) => state.patients);
  const fetchPatients = usePatientStore((state) => state.fetchPatients);

  useEffect(() => {
    fetchPatients();
  }, [fetchPatients]);

  return (
    <main className="p-4 space-y-6">
      {/* Header Section */}
      <section className="flex flex-wrap justify-between px-4 items-center">
        <div className="flex items-center space-x-2">
          <MdMonitor className="text-accentMain size-6" />
          <h2 className="text-xl font-bold text-gray-800">Live Updates</h2>
        </div>
        <div className="flex items-center space-x-2 text-gray-500">
          <LuUsers className="size-5" />
          <p className="text-sm">{patients.length} Active Patient(s)</p>
        </div>
      </section>

      {/* Legend Section */}
      <section className="space-y-2">
        <h3 className="text-sm font-medium text-gray-600">Status Legend</h3>
        <div className="flex gap-4 overflow-x-auto pb-2">
          <StatusCard />
        </div>
      </section>

      {/* Patients Display (To be implemented) */}
      <section className="mt-6">
        <div className="w-full max-w-7xl mt-4 min-h-[40dvh] mx-auto px-4">
      {patients.length ? (
        <ActivePatientCard />
      ) : (
        <p className="text-center text-gray-500 py-8">No active patients yet</p>
      )}
    </div>
      </section>
    </main>
  );
}
