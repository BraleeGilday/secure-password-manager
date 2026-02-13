// for pwd gen modal
import { useState } from "react";
// ------

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
        <button className="pwd-gen-btn" onClick={openPwdGenModal}>
        generator
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