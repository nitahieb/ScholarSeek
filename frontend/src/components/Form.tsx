import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/Form.css"


function Form({route, method}: {route: string, method: string}) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [errorMsg, setErrorMsg] = useState("");
    const navigate = useNavigate();

    const name = method === "login" ? "Login" : "Register"; 

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        setLoading(true);
        e.preventDefault();

        // Passwords must match for registration
        if (method === "register" && password !== confirmPassword) {
            setErrorMsg("Passwords do not match.");
            setLoading(false);
            return;
        }

        try {
            const response = await api.post(route, {username, password, email});
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, response.data.access);
                localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
                navigate("/");
            } else {
                navigate("/login");
            }
        } catch (error: unknown) {
            const errorResponse = error as { response?: { data?: { username?: string[] } } };
            if (
                method === "register" &&
                errorResponse?.response?.data?.username &&
                errorResponse.response.data.username[0].includes("already exists")
            ) {
                setErrorMsg("An account with that username already exists.");
            } else {
                setErrorMsg("Error: " + (error?.response?.data?.detail || error.message));
            }
        } finally {
            setLoading(false);
        }
    }

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>{name}</h1>
            {errorMsg && <div className="form-error">{errorMsg}</div>}
            <input 
                className="form-input" 
                type="text" 
                placeholder="Username" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} required 
            />
            {method === "register" && (
                <>
                    <input
                        className="form-input"
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)} required
                    />
                    <input
                        className="form-input"
                        type="password"
                        placeholder="Confirm Password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                    />
                </>
            )}
            <input 
                className="form-input" 
                type="password" 
                placeholder="Password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} required 
            />
            <button className="form-button" type="submit" disabled={loading}>
                {loading ? "Loading..." : name}
            </button>   
        </form>
    );
}

export default Form