import Card from "../components/Card"

import PasswordGenerator from "../components/PasswordGenerator"

export default function Welcome() {
    let welcomeText = "Welcome to Secure Password Manager (SPM)! New users: click 'register' to get started."

    return(
        <>
        <Card content={welcomeText} />
        <div>
            <PasswordGenerator />
        </div>
        </>
    )
}