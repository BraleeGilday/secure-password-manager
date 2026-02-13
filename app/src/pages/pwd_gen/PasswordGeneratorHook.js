import { useState } from 'react';
import axios from 'axios';

const DATABASE_URL = "http://127.0.0.1:8000"

// custom hook to handle copy, change, submit for password generator
// add loading? 
export const PasswordGeneratorHook = () => {
    const getToken = () => localStorage.getItem('token'); //will need to have token passed once setup
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
        const { name, value, type, checked } = event.target;
        setFormData({
            ...formData,
            [name]: type === "checkbox" ? checked : value,
        });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post(`${DATABASE_URL}/spm/password/generate`, formData);
            const generatedPassword = response.data;
            setPassword(generatedPassword.password);
        } catch (error) {
            console.log("Error generating password");
        }
    };

    return {
        formData,
        password,
        copiedText,
        handleChange,
        handleCopy,
        handleSubmit
    };
};