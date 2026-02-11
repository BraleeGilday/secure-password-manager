import { useState } from "react"
import axios from 'axios';

export default function PasswordGenerator() {
    const getToken = () => localStorage.getItem('token');
    const [formData, setFormData] = useState({
        length: 16,
        has_symbols: true,
        has_numbers: true,
        mixed_case: true,
    })

    const [password, setPassword] = useState(null);

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
            const response = await axios.post("http://127.0.0.1:8000/spm/password/generate", formData);
            const generatedPassword = response.data;
            setPassword(generatedPassword.password);
        } catch (error) {
            console.log("Error generating password");
        }
    }

    return (
        <>
        <div className="pwd-gen-box">
            {!password ? (
                <>
                </>
            ) : (
                <>
                <div>
                    {password}
                </div>
                </>
            )}
        <form onSubmit={handleSubmit}>
            <button type="submit">{!password ? 'Generate' : 'Refresh'}</button>
            <label>Password Length</label>
            <input
                type="range"
                name="length"
                min="8"
                max="64"
                value={formData.length}
                onChange={handleChange}
            />
            <label>Symbols</label>
            <input 
                type="checkbox"
                name="has_symbols"
                checked={formData.has_symbols}
                onChange={handleChange}
            />
            <label>Numbers</label>
            <input 
                type="checkbox"
                name="has_numbers"
                checked={formData.has_numbers}
                onChange={handleChange}
            />
            <label>Mixed case</label>
            <input 
                type="checkbox"
                name="mixed_case"
                checked={formData.mixed_case}
                onChange={handleChange}
            />
        </form>
        </div>
        </>
    )
}