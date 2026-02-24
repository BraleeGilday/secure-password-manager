import Card from "../components/Card";

import PasswordGeneratorButton from "./pwd_gen/PasswordGeneratorButton";

export default function Welcome() {
    // pwd gen modal will need to be relocated to appropriate page (credentials)


    let welcomeText = "Welcome to Secure Password Manager (SPM)! New users: click 'register' to get started."

    return(
        <div className="page-center">
            <Card content={welcomeText} />
            
            <PasswordGeneratorButton />
        </div>
    )
}