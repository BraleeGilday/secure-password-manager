import Card from "../components/Card";

export default function Welcome() {

    let welcomeText = (
        <div style={{textAlign: "center", padding: "2px"}}>
            <p>Welcome to Secure Password Manager (SPM)!</p>
            <p>New users: click <strong>register</strong> to get started."</p>
        </div>
        )

    return (
        <div className="page-center">
            <Card content={welcomeText} />
        </div>
    )
}