import { useRef, useEffect } from 'react';
import { createPortal } from "react-dom";

export default function PasswordGeneratorModal({close, content}) {
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
        <dialog className="pwd-gen-dialog" onClose={handleClose} ref={dialog}>
            {content}
            <form method="dialog">
                <button type="button" onClick={handleClose}>Close</button>
            </form>
        </dialog>,
        document.getElementById('modal')
    );
}