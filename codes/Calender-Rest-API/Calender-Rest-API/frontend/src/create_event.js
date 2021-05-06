import React from 'react';
import 'antd/dist/antd.css';
import {Modal, Button} from 'antd';
import AddForm from "./add_event_form";

const AddEvent = ({}) => {
    const [visible, setVisible] = React.useState(false);
    const [confirmLoading, setConfirmLoading] = React.useState(false);
    const [modalText, setModalText] = React.useState('Content of the modal');

    const showModal = () => {
        setVisible(true);
    };

    const handleOk = () => {
        setConfirmLoading(true);
        setVisible(false);
        setConfirmLoading(false);
    };

    const handleCancel = () => {
        console.log('Clicked cancel button');
        setVisible(false);
    };

    return (
        <>
            <button onClick={showModal}
                    className="btn btn-sm btn-outline-info">Edit
            </button>
            <Modal
                title="Edit Project Details"
                visible={visible}
                onOk={handleOk}
                confirmLoading={confirmLoading}
                onCancel={handleCancel}
            >
                <AddForm />
            </Modal>
        </>
    );
};

export default AddEvent;