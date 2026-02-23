import { useState } from "react";

import PasswordGenerator from "./PasswordGenerator";
import Modal from "../../components/Modal";

export default function PasswordGeneratorButton() {
    const [activeModal, setActiveModal] = useState(false);

    const openPwdGenModal = () => {
        setActiveModal(true);
    }

    const closePwdGenModal = () => {
        setActiveModal(false);
    }

    return (
        <>
        <button type="button" className="pwd-gen-btn" onClick={openPwdGenModal}>
        Generator
        </button>
        {activeModal && (
            <Modal 
                close={closePwdGenModal}
                dialogStyle={"pwd-gen-dialog"}
                content={<PasswordGenerator />}
            />
        )}
        </>
    )
}
