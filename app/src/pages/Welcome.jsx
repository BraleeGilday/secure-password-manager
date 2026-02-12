import Card from "../components/Card";

import PasswordGenerator from "../components/PasswordGenerator";
import PasswordGeneratorButton from "../components/PasswordGeneratorButton";
export default function Welcome() {
    // pwd gen modal will need to be relocated to appropriate page (credentials)


    let welcomeText = "Welcome to Secure Password Manager (SPM)! New users: click 'register' to get started."

    return(
        <>
        <Card content={welcomeText} />
        
        <PasswordGeneratorButton />
        
        </>
    )
}