import { useRef, useEffect } from 'react';
import { createPortal } from "react-dom";

export default function PasswordGeneratorModal() {
    const dialog = useRef();

    useEffect(() => {
        if (dialog.current) {
            dialog.current.showModal();
        }
    }, []);

    const handleClose = () => {
        dialog.current.close();
        if (close) close();
    };
    
    return createPortal(
        <dialog onClose={handleClose} ref={dialog}>
            <form method="dialog">
                <button onClick={handleClose}>Close</button>
            </form>
        </dialog>,
        document.getElementById('modal')
    );
}