import React from 'react'

export default function DoctorLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-gray-50 min-h-screen">
      {/* You can add a Sidebar or Topbar here */}
      {children}
    </div>
  )
}