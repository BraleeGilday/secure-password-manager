import Card from "../components/Card";

export default function Welcome() {

<<<<<<< HEAD
    let welcomeText = (
        <div style={{textAlign: "center", padding: "2px"}}>
            <p>Welcome to Secure Password Manager (SPM)!</p>
            <p>New users: click <strong>register</strong> to get started."</p>
        </div>
        )
=======
    let welcomeText = "Welcome to Secure Password Manager (SPM)! New users: click 'register' to get started."
>>>>>>> a747d1c (remove dark mode, fix logout button, change search bar color to magenta, remove pwd gen from welcome)

    return(
        <div className="page-center">
            <Card content={welcomeText} />
        </div>

    )
}