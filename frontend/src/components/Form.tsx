import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import axios from "axios";

function Form({ route, method }: { route: string; method: string }) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [password, setPassword] = useState("");
    const [registrationCode, setRegistrationCode] = useState("");
    const [loading, setLoading] = useState(false);
    const [errorMsg, setErrorMsg] = useState("");
    const navigate = useNavigate();

    const name = method === "login" ? "Login" : "Register";

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        setLoading(true);
        e.preventDefault();

        if (method === "register" && password !== confirmPassword) {
            setErrorMsg("Passwords do not match.");
            setLoading(false);
            return;
        }

        try {
            const data: Record<string, string> = { username, password, email };
            if (method === "register") {
                data.registration_code = registrationCode;
            }
            const response = await api.post(route, data);
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, response.data.access);
                localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
                navigate("/");
            } else {
                navigate("/login");
            }
        } catch (error) {
            let errorMessage = "An unknown error occurred.";
            if (axios.isAxiosError(error)) {
                if (method === "register" && error.response?.data?.username) {
                    const usernameError = error.response.data.username[0];
                    if (usernameError.includes("already exists")) {
                        errorMessage = "An account with that username already exists.";
                    }
                } else if (error.response?.data?.detail) {
                    errorMessage = "Error: " + error.response.data.detail;
                } else if (error.message) {
                    errorMessage = "Error: " + error.message;
                }
            } else if (error instanceof Error) {
                errorMessage = "Error: " + error.message;
            }
            setErrorMsg(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card" style={{ maxWidth: '400px', width: '100%' }}>
            <h1 style={{ textAlign: 'center', marginBottom: 'var(--spacing-lg)' }}>{name}</h1>

            <form onSubmit={handleSubmit}>
                {errorMsg && (
                    <div style={{
                        backgroundColor: '#FEF2F2',
                        color: 'var(--color-error)',
                        padding: 'var(--spacing-sm)',
                        borderRadius: 'var(--radius-md)',
                        marginBottom: 'var(--spacing-md)',
                        fontSize: '0.875rem'
                    }}>
                        {errorMsg}
                    </div>
                )}

                <div className="input-group">
                    <label className="input-label" htmlFor="username">Username</label>
                    <input
                        className="input-field"
                        type="text"
                        id="username"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>

                {method === "register" && (
                    <div className="input-group">
                        <label className="input-label" htmlFor="email">Email</label>
                        <input
                            className="input-field"
                            type="email"
                            id="email"
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                )}

                <div className="input-group">
                    <label className="input-label" htmlFor="password">Password</label>
                    <input
                        className="input-field"
                        type="password"
                        id="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>

                {method === "register" && (
                    <>
                        <div className="input-group">
                            <label className="input-label" htmlFor="confirmPassword">Confirm Password</label>
                            <input
                                className="input-field"
                                type="password"
                                id="confirmPassword"
                                placeholder="Confirm Password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                            />
                        </div>
                        <div className="input-group">
                            <label className="input-label" htmlFor="registrationCode">Registration Code</label>
                            <input
                                className="input-field"
                                type="text"
                                id="registrationCode"
                                placeholder="Registration Code"
                                value={registrationCode}
                                onChange={(e) => setRegistrationCode(e.target.value)}
                                required
                            />
                        </div>
                    </>
                )}

                <button
                    className="btn btn-primary"
                    type="submit"
                    disabled={loading}
                    style={{ width: '100%', marginTop: 'var(--spacing-sm)' }}
                >
                    {loading ? "Loading..." : name}
                </button>

                <div style={{ marginTop: "var(--spacing-lg)", textAlign: "center", fontSize: '0.875rem' }}>
                    {method === "login" ? (
                        <span>
                            New to PubMed Author Finder?{" "}
                            <button
                                type="button"
                                onClick={() => navigate("/register")}
                                style={{
                                    background: "none",
                                    border: "none",
                                    padding: 0,
                                    font: "inherit",
                                    cursor: "pointer",
                                    color: 'var(--color-primary)',
                                    fontWeight: 600
                                }}
                            >
                                Sign up
                            </button>
                        </span>
                    ) : (
                        <span>
                            Already have an account?{" "}
                            <button
                                type="button"
                                onClick={() => navigate("/login")}
                                style={{
                                    background: "none",
                                    border: "none",
                                    padding: 0,
                                    font: "inherit",
                                    cursor: "pointer",
                                    color: 'var(--color-primary)',
                                    fontWeight: 600
                                }}
                            >
                                Log in
                            </button>
                        </span>
                    )}
                </div>
            </form>
        </div>
    );
}

export default Form;
