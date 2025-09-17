import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/Form.css";
import Header from "./Header";
import Footer from "./Footer";
import "./PubMedSearch.css";

function Form({ route, method }: { route: string; method: string }) {
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

        if (method === "register" && password !== confirmPassword) {
            setErrorMsg("Passwords do not match.");
            setLoading(false);
            return;
        }

        try {
            const response = await api.post(route, { username, password, email });
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, response.data.access);
                localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
                navigate("/");
            } else {
                navigate("/login");
            }
        } catch (error: any) {
            if (
                method === "register" &&
                error?.response?.data?.username &&
                error.response.data.username[0].includes("already exists")
            ) {
                setErrorMsg("An account with that username already exists.");
            } else {
                setErrorMsg("Error: " + (error?.response?.data?.detail || error.message));
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="pubmed-search">
            <Header />
            <main className="main-content">
                <form onSubmit={handleSubmit} className="form-container">
                    <h1>{name}</h1>
                    {errorMsg && <div className="form-error">{errorMsg}</div>}
                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            className="form-input"
                            type="text"
                            id="username"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    {method === "register" && (
                        <>
                            <div className="form-group">
                                <label htmlFor="email">Email</label>
                                <input
                                    className="form-input"
                                    type="email"
                                    id="email"
                                    placeholder="Email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="confirmPassword">Confirm Password</label>
                                <input
                                    className="form-input"
                                    type="password"
                                    id="confirmPassword"
                                    placeholder="Confirm Password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    required
                                />
                            </div>
                        </>
                    )}
                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            className="form-input"
                            type="password"
                            id="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button className="form-button" type="submit" disabled={loading}>
                        {loading ? "Loading..." : name}
                    </button>
                    <div style={{ marginTop: "18px", textAlign: "center" }}>
                        {method === "login" ? (
                            <span>
                                New to PubMed Author Finder?{" "}
                                <button
                                    type="button"
                                    className="form-link"
                                    onClick={() => navigate("/register")}
                                    style={{ background: "none", border: "none", padding: 0, font: "inherit", cursor: "pointer" }}
                                >
                                    Sign up
                                </button>
                            </span>
                        ) : (
                            <span>
                                Already have an account?{" "}
                                <button
                                    type="button"
                                    className="form-link"
                                    onClick={() => navigate("/login")}
                                    style={{ background: "none", border: "none", padding: 0, font: "inherit", cursor: "pointer" }}
                                >
                                    Log in
                                </button>
                            </span>
                        )}
                    </div>
                </form>
            </main>
            <Footer />
        </div>
    );
}

export default Form;