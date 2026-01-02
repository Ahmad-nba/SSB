"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/Features/auth/hooks/useAuth";

export default function ProtectedRoute({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isLoggedIn, hasHydrated } = useAuth();
  const router = useRouter();
  const [canRender, setCanRender] = useState(false);

  useEffect(() => {
    if (!hasHydrated) return;

    if (!isLoggedIn) {
      router.replace("/");
    } else {
      setCanRender(true);
    }
  }, [hasHydrated, isLoggedIn, router]);

  if (!hasHydrated || !canRender) {
    <div className="flex items-center justify-center min-h-screen text-gray-600">
      Loading...
    </div>;
  }

  return <>{children}</>;
}
