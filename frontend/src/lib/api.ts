import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL.replace("http://localhost:8000", "/localhost:8000"),
  headers: { "Content-Type": "application/json" },
});


export default api;
