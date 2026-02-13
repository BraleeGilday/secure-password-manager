import { PasswordGeneratorHook } from "./PasswordGeneratorHook";

const Checkbox = ({label, name, checked, onChange}) => (
    <>
    <label>{label}</label>
    <input 
        type="checkbox"
        name={name}
        checked={checked}
        onChange={onChange}
    />
    </>
)

export default function PasswordGenerator() {
    const {
        formData, password, copiedText,
        handleChange, handleCopy, handleSubmit
    } = PasswordGeneratorHook();

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
                Password Length
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
            <Checkbox label="Symbols" name="has_symbols" checked={formData.has_symbols} onChange={handleChange} />
            <Checkbox label="Numbers" name="has_numbers" checked={formData.has_numbers} onChange={handleChange} />
            <Checkbox label="Mixed case" name="mixed_case" checked={formData.mixed_case} onChange={handleChange} />
        </div>
        </div>
        </>
    )
}