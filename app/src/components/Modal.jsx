import { useRef, useEffect } from 'react';
import { createPortal } from "react-dom";

// Modal pop up for potentially different things (used currently for password generator)
// could potential be expaned for alerts (delete, add, error, etc)

export default function Modal({close, dialogStyle, content}) {
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
        <dialog className={dialogStyle ? dialogStyle : ""} onClose={handleClose} ref={dialog}>
            {content}
            <form method="dialog">
                <button type="button" onClick={handleClose}>Close</button>
            </form>
        </dialog>,
        document.getElementById('modal')
    );
}