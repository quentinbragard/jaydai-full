// src/extension/welcome/hooks/useAuthState.ts
import { useState, useEffect } from 'react';
import { AuthState } from '@/types';
import { authService } from '@/services/auth/AuthService';
import { trackEvent, setAmplitudeUserId, EVENTS } from '@/utils/amplitude';

export function useAuthState() {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null
  });

  useEffect(() => {
    const unsubscribe = authService.subscribe((state) => {
      setAuthState(state);
      
      // Set Amplitude user ID when authenticated
      if (state.user && state.isAuthenticated) {
        setAmplitudeUserId(state.user.id);
      }
    });
    
    return () => {
      unsubscribe();
    };
  }, []);

  const handleSignOut = async () => {
    try {
      trackEvent(EVENTS.SIGNOUT);
      await authService.signOut();
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  return { authState, handleSignOut };
}

