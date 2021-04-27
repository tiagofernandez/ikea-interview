import Button from "@material-ui/core/Button";
import Snackbar from "@material-ui/core/Snackbar";
import CloudUploadIcon from "@material-ui/icons/CloudUpload";
import React from "react";

import api from "../api";
import AppContext from "../AppContext";

export default function UploadButton({ onError, onSuccess, target }) {
    const { dispatch } = React.useContext(AppContext);
    const fileInput = React.useRef();

    const [errorMessage, setErrorMessage] = React.useState(null);

    return (
        <>
            <Button
                color="primary"
                startIcon={<CloudUploadIcon />}
                variant="contained"
                onClick={() => fileInput.current.click()}
            >
                Upload {target}
            </Button>
            <input
                accept=".json"
                type="file"
                ref={fileInput}
                style={{ display: "none" }}
                onChange={(event) => {
                    const file = event.target.files[0];
                    const reader = new FileReader();
                    reader.addEventListener("load", async (event) => {
                        try {
                            const { result } = event.target;
                            const json = JSON.parse(result);

                            const data = await api.upload(target, json);
                            dispatch({ type: `refresh-${target}`, data });

                            if (onSuccess) {
                                onSuccess(data);
                            }
                            setErrorMessage(`Uploaded ${target}`);
                        } catch (err) {
                            if (onError) {
                                onError(err);
                            }
                            const message = err?.response?.data?.error;
                            setErrorMessage(message || "Invalid JSON file");
                        }
                    });
                    reader.readAsText(file);
                    event.target.value = null; // Reset file input.
                }}
            />
            <Snackbar
                autoHideDuration={3000}
                open={errorMessage !== null}
                message={errorMessage}
                onClose={() => setErrorMessage(null)}
            />
        </>
    );
}
