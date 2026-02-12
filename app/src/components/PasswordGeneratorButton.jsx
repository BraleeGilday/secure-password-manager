// for pwd gen modal
import { useState } from "react";
// ------
import PasswordGeneratorModal from "./PasswordGeneratorModal";
import PasswordGenerator from "./PasswordGenerator";

export default function PasswordGeneratorButton() {
     // PWD GEN MODAL
    const [activeModal, setActiveModal] = useState(false);

    const openPwdGenModal = () => {
        setActiveModal(true);
    }

    const closePwdGenModal = () => {
        setActiveModal(false);
    }

    // -------------
    return (
        <>
        <button className="pwd-gen-btn" onClick={openPwdGenModal}>
        generator
        </button>
        {activeModal && (
            <PasswordGeneratorModal 
                close={closePwdGenModal}
                content={<PasswordGenerator />}
            />
        )}
        </>
    )
}