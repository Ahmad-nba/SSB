// import axios from "axios";
// import { useAuthStore } from "../store/useAuthStore";

// const API_URL = "http://localhost:8000/api/auth/login/";

// export async function handleLogin(email: string, password: string) {
//   try {
//     const response = await axios.post(API_URL, { email, password });

//     const { token, user } = response.data;

//     useAuthStore.getState().login(user, token);

//     return { success: true, user, token };
//   } catch (error: any) {
//     console.error("Login failed:", error.response?.data || error.message);
//     return { success: false, error: error.response?.data || "Login failed" };
//   }
// }
// export async function handleLogin(email: string, password: string) {
//   try {
//     const response = await axios.post(API_URL, { email, password });

//     const { access, refresh, user } = response.data;

//     // ✅ Pass tokens properly
//     useAuthStore.getState().login(user.email, access); // or modify based on your store signature

//     return { success: true, user, access, refresh };
//   } catch (error: any) {
//     console.error("Login failed:", error.response?.data || error.message);
//     return { success: false, error: error.response?.data || "Login failed" };
//   }
// }
