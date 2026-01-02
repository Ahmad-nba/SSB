import { useEffect } from "react";
import { useAuthStore } from "../store/useAuthStore";

export const useAuth = () => {
  const { user, role, token, hasHydrated, loadUser } = useAuthStore();

  // Debug log to track hydration and user state
  console.log("Hydrated:", hasHydrated, "User:", user, "Token:", token, "Role:", role);

  // Run once after hydration to load user if needed
  useEffect(() => {
    if (!hasHydrated) return;

    if (!user) {
      loadUser();
    }
  }, [hasHydrated, user, loadUser]);

  const fullName = user?.username || user?.email || "Guest";

  // Simplified: only depends on user object
  const isLoggedIn = !!user;

  return { user, role, token, fullName, isLoggedIn, hasHydrated };
};
