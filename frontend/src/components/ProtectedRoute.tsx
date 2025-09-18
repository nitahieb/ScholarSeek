import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import {type JSX, useState, useEffect, useCallback } from "react";

function ProtectedRoute({ children }: { children: JSX.Element }) {

    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

    const refreshToken = useCallback(async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);
        try {
            const res = await api.post("api/token/refresh/", { 
                refresh: refreshToken 
            });
            if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                setIsAuthenticated(true);
            } else {
                setIsAuthenticated(false);
            }

        } catch (error) {
            console.error("Error refreshing token:", error);
            setIsAuthenticated(false);
        }
    }, []);

    const authenticate = useCallback(async () => {
        setIsAuthenticated(null);
        try {
            const token = localStorage.getItem(ACCESS_TOKEN);
            if (!token) {
                setIsAuthenticated(false);
                return;
            }
            const decoded = jwtDecode(token);
            const tokenExpiration = decoded.exp;
            const now = Date.now() / 1000;
            
            if (tokenExpiration && tokenExpiration < now) {
                await refreshToken();
            } else {
                setIsAuthenticated(true);
            }
        } catch (error) {
            setIsAuthenticated(false);
        }
    }, [refreshToken]);

    useEffect(() => {
        authenticate().catch((error) => {
            setIsAuthenticated(false);
            console.error("Error during authentication:", error);
        });
    }, [authenticate]);

    if (isAuthenticated === null) {
        return <div>Loading...</div>;
    }

    return isAuthenticated ? children : <Navigate to="/login" />;
}

export default ProtectedRoute;