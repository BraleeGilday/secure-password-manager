import { useState } from "react"
import axios from 'axios';

export default function PasswordGenerator() {
    const getToken = () => localStorage.getItem('token');
    const [copiedText, setCopiedText] = useState(false);
    const [formData, setFormData] = useState({
        length: 16,
        has_symbols: true,
        has_numbers: true,
        mixed_case: true,
    })

    const [password, setPassword] = useState(null);

    const handleCopy = async () => {
        try {
            await navigator.clipboard.writeText(password);
            setCopiedText(true);

            setTimeout(() => setCopiedText(false), 3000);
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
            {password && (
                <div className="pwd-box">
                    <span id='pwd-txt'>{password}</span>
                    <button onClick={handleCopy} className="copy-btn">{copiedText ? 'Copied!': 'Copy'}</button>
                </div>
            )}
        <div className="spacer">
            <label>
                <span>Password Length</span>
            </label>
            <div id ="length-display">{formData.length}</div>
            <input
                type="range"
                name="length"
                min="8"
                max="64"
                value={formData.length}
                onChange={handleChange}
            />
            <button type="button" onClick={handleSubmit}>{!password ? 'Generate' : 'Refresh'}</button>
        </div>
        <div className="spacer">
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
        </div>
        </div>
        </>
    )
}