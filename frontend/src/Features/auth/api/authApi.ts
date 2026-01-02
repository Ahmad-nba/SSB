// Central API functions for authentication
import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

// export async function loginUser(email: string, password: string) {
//   const res = await axios.post(`${API_BASE}/auth/login/`, { email, password });
//   return res.data;
// }

// export async function loginUser(email: string, password: string) {
//   try {
//     const res = await axios.post(
//       `${API_BASE}/auth/login/`,
//       { email, password },
//       { headers: { "Content-Type": "application/json" } }
//     );
//     return res.data;
//   } catch (err: any) {
//     if (err.response) {
//       console.error("Login error response:", err.response.data);
//       throw new Error(err.response.data.detail || "Login failed");
//     } else {
//       throw err;
//     }
//   }
// }

export async function loginUser(email: string, password: string) {
  try {
    const res = await axios.post(
      `${API_BASE}/auth/login/`,
      { email, password },
      { headers: { "Content-Type": "application/json" } }
    );

    return res.data;
  } catch (err: unknown) {
    if (axios.isAxiosError<AuthErrorResponse>(err)) {
      const message =
        err.response?.data?.detail ?? "Login failed";

      console.error("Login error:", err.response?.data);
      throw new Error(message);
    }

    // Non-Axios error (should be rare)
    throw new Error("Unexpected error occurred during login");
  }
}



export async function logoutUser(refresh: string) {
  // optional if you implement logout on backend
  const res = await axios.post(`${API_BASE}/auth/logout/`, { refresh });
  return res.data;
}

export async function fetchCurrentUser(token: string) {
  const res = await axios.get(`${API_BASE}/auth/me/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}
