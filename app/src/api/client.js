import axios from "axios";

// local
const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// deployment test
// const api = axios.create({
//   baseURL: "",
// });

export default api;
