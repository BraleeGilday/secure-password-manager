import { useRef, useEffect } from 'react';
import { createPortal } from "react-dom";

// Modal pop up

// params 
//  close: setActiveModal(false) function; 
//  dialogStyle: css class style; 
//  content:component or whatever

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
                <button className='modal-btn' type="button" title="close" onClick={handleClose}>x</button>
            </form>
        </dialog>,
        document.getElementById('modal')
    );
}