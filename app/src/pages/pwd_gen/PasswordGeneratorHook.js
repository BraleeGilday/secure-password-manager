import { useState } from 'react';
import api from "../../api/client.js"


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

  const handleCopy = async (copiedPwd) => {
    if (!password) return;
    if (!copiedPwd) return;
    
    // if (navigator.clipboard && window.isSecureContext) {
    //   try {
    //     await navigator.clipboard.writeText(password);
    //     triggerCopySuccess();
    //     return;
    //   } catch (err) {
    //     console.error("Clipboard API failed, trying fallback", err);
    //   }
    // }
    // gemini workaround for HTTP
    // 2. Fallback for HTTP
    try {
      const textArea = document.createElement("textarea");
      textArea.value = copiedPwd;
      
      // Keep it hidden from the user
      textArea.style.position = "absolute";
      textArea.style.left = "-9999px";
      textArea.style.top = "0";
      
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      
      const successful = document.execCommand("copy");
      console.log(textArea.value);
      document.body.removeChild(textArea);

      if (successful) {
        triggerCopySuccess();
      }
    } catch (err) {
      console.error("Fallback copy failed", err);
    }
  };

  const triggerCopySuccess = () => {
    setCopiedText(true);
    setTimeout(() => setCopiedText(false), 2000);
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