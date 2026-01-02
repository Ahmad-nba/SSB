import { create } from "zustand";
import { persist } from "zustand/middleware";
import { User } from "../types/type";
import { loginUser, logoutUser, fetchCurrentUser } from "../api/authApi";

interface AuthStore {
  user: User | null;
  role: string;
  token: string | null;
  refresh: string | null;
  hasHydrated: boolean;
  setHydrated: () => void;
  isLoggedIn: () => boolean;

  login: (email: string, password: string) => Promise<{
    success: boolean;
    user?: User;
    error?: string;
  }>;

  logout: () => Promise<{
    success: boolean;
    error?: string;
  }>;

  loadUser: () => Promise<{
    success: boolean;
    user?: User;
    error?: string;
  }>;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      role: "GUEST",
      token: null,
      refresh: null,
      hasHydrated: false,

      setHydrated: () => set({ hasHydrated: true }),

      // Simplified: only check if user object exists
      isLoggedIn: () => !!get().user,

      login: async (email, password) => {
        try {
          const data = await loginUser(email, password);
          console.log("Login response:", data);

          if (!data.user) {
            return { success: false, error: "Invalid response from server" };
          }

          set({
            user: data.user,
            role: data.user.role || "GUEST",
            token: data.access, // still store token if needed
            refresh: data.refresh,
          });

          return { success: true, user: data.user };
        } catch (error: any) {
          console.error("Login error:", error);
          return {
            success: false,
            error: error.response?.data || "Login failed",
          };
        }
      },

      logout: async () => {
        try {
          const refresh = get().refresh;
          if (refresh) {
            await logoutUser(refresh);
          }
        } catch (err) {
          console.warn("Logout error:", err);
        } finally {
          set({ user: null, role: "GUEST", token: null, refresh: null });
        }
        return { success: true };
      },

      loadUser: async () => {
        try {
          const data = await fetchCurrentUser(get().token || "");

          if (!data.user) {
            return { success: false, error: "Invalid response from server" };
          }

          set({
            user: data.user || data,
            role: data.user?.role || data.role || "GUEST",
          });

          return { success: true, user: data.user || data };
        } catch (err) {
          console.warn("Token expired or invalid, clearing session");
          set({ user: null, role: "GUEST", token: null, refresh: null });
          return { success: false, error: "Failed to load user" };
        }
      },
    }),
    {
      name: "auth-store",
      partialize: (state) => ({
        user: state.user,
        role: state.role,
        token: state.token,
        refresh: state.refresh,
      }),
      onRehydrateStorage: () => (state, error) => {
        if (error) console.warn("Rehydrate error:", error);
        state?.setHydrated();
      },
    }
  )
);
