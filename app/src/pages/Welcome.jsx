import Card from "../components/Card";

export default function Welcome() {

    let welcomeText = "Welcome to Secure Password Manager (SPM)! New users: click 'register' to get started."

    return(
        <div className="page-center">
            <Card content={welcomeText} />
        </div>
    )
}