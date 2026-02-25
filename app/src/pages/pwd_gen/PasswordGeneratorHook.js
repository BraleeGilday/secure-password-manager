import { useState } from 'react';
// import api
import axios from 'axios';

// const DATABASE_URL = "http://127.0.0.1:8000"
// for use with nginx
const BACKEND_URL = "";
// custom hook to handle copy, change, submit for password generator
export const PasswordGeneratorHook = () => {
  const getToken = () => localStorage.getItem("access_token");
  const [password, setPassword] = useState(null);
  const [copiedText, setCopiedText] = useState(false);
  const [formData, setFormData] = useState({
    length: 16,
    has_symbols: true,
    has_numbers: true,
    mixed_case: true,
  });

  const handleCopy = async () => {
    if (!password) return;
    try {
      await navigator.clipboard.writeText(password);
      setCopiedText(true);

      setTimeout(() => setCopiedText(false), 2000);
    } catch (error) {
      console.error("Failed to copy", error);
    }
  };

  const handleChange = (event) => {
    const { name, value, valueAsNumber, type, checked } = event.target;
    setFormData({
      ...formData,
      [name]:
        type === "checkbox"
          ? checked
          : name === "length"
            ? valueAsNumber
            : value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const token = getToken();

    try {
      const response = await api.post("/spm/password/generate", formData, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      setPassword(response.data.password);
    } catch (error) {
      console.log("Error generating password", error?.response?.data || error);
    }
  };

  return {
    formData,
    password,
    copiedText,
    handleChange,
    handleCopy,
    handleSubmit,
  };
};