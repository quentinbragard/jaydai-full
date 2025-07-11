// 🔹 Open welcome page when the extension is installed
function createContextMenus() {
  chrome.contextMenus.removeAll(() => {

    chrome.contextMenus.create({
      id: 'create_block',
      title: 'Create a Jaydai Block',
      contexts: ['all'],
    });
    chrome.contextMenus.create({
      id: 'insert_block',
      title: 'Insert a Jaydai Block',
      contexts: ['all'],
    });
  });
}

chrome.runtime.onInstalled.addListener(() => {
  chrome.tabs.create({ url: 'welcome.html' });
  createContextMenus();
});

// Recreate menus whenever Chrome starts
chrome.runtime.onStartup.addListener(createContextMenus);

// Also create menus when the service worker loads
createContextMenus();

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (!tab || !tab.id) return;
  if (info.menuItemId === 'create_block') {
    chrome.tabs.sendMessage(tab.id, {
      action: 'openCreateBlockDialog',
      content: info.selectionText || ''
    });
  } else if (info.menuItemId === 'insert_block') {
    chrome.tabs.sendMessage(tab.id, { action: 'openInsertBlockDialog' });
  }
});


// 🔹 Open welcome page only when the extension is newly installed, not on updates
//chrome.runtime.onInstalled.addListener((details) => {
  // Only open the welcome page for new installations, not updates
  //if (details.reason === 'install') {
  //    chrome.tabs.create({ url: 'welcome.html' });
  //}
//});

// Track active monitoring tabs (if still needed)
const monitoredTabs = new Set();

// Main message listener
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    const actions = {
        // Auth actions
        googleSignIn: () => googleSignIn(sendResponse),
        emailSignIn: () => emailSignIn(request.email, request.password, sendResponse),
        signUp: () => signUp(request.email, request.password, request.name, sendResponse),
        getAuthToken: () => sendAuthToken(sendResponse),
        refreshAuthToken: () => refreshAndSendToken(sendResponse),
        
        // Locale actions
        getUserLocale: () => {
            // Get user's preferred locale
            const locale = chrome.i18n.getUILanguage();
            sendResponse({ success: true, locale });
            return false;
        },
        
        // Network monitoring actions - simplified
        'start-network-monitoring': () => {
            // Just return success since the injected interceptor will handle actual monitoring
            sendResponse({ success: true });
            return false;
        },
        'stop-network-monitoring': () => {
            // Just return success
            sendResponse({ success: true }); 
            return false;
        },
        'network-request-captured': () => {
            // Pass through the captured request to content script if needed
            if (sender.tab?.id) {
                chrome.tabs.sendMessage(sender.tab.id, {
                    action: 'network-request-captured',
                    data: request.data
                });
            }
            sendResponse({ success: true });
            return false;
        }
    };

    if (actions[request.action]) {
        const result = actions[request.action]();
        // For async handlers that don't explicitly return false,
        // keep the message channel open by returning true
        return result === false ? false : true;
    } else {
        sendResponse({ success: false, error: "Invalid action" });
        return false; // Ensures message channel is closed
    }
});

/* ==========================================
 🔹 SIGN IN FLOWS
========================================== */
async function emailSignIn(email, password, sendResponse) {
    try {
      
      const response = await fetch(`${process.env.VITE_API_URL}/auth/sign_in`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
  
      const data = await response.json();
      
      if (!response.ok) {
        console.error("❌ Email Sign-In failed:", data);
        sendResponse({ 
          success: false, 
          error: data.detail || "Invalid email or password" 
        });
        return;
      }
      
      // Validate required data
      if (!data.session || !data.session.access_token || !data.session.refresh_token) {
        console.error("❌ Invalid response from sign-in endpoint (missing session data):", data);
        sendResponse({ 
          success: false, 
          error: "Server returned invalid authentication data" 
        });
        return;
      }
      
      
      
      // Store session data first (tokens)
      storeAuthSession(data.session);
      
      // Then store user data
      if (data.user) {
        storeUser(data.user);
      } else {
        console.warn("⚠️ No user data returned from sign-in endpoint");
      }
      
      // Response should be sent after storage operations
      sendResponse({ 
        success: true, 
        user: data.user, 
        access_token: data.session.access_token 
      });
    } catch (error) {
      console.error("❌ Error in email sign-in:", error);
      sendResponse({ 
        success: false, 
        error: error.message || "Unable to connect to authentication service" 
      });
    }
    
    return true; // Keep channel open for async response
  }
  
  function signUp(email, password, name, sendResponse) {
    
    // Send request to our backend API
    fetch(`${process.env.VITE_API_URL}/auth/sign_up`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, name }),
    })
    .then(response => {
      // Handle non-JSON responses
      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        throw new Error("Server returned non-JSON response");
      }
      return response.json();
    })
    .then(data => {
      if (!data.success) {
        throw new Error(data.detail || data.error || "Sign-up failed");
      }
      
      
      // Store user data
      if (data.user) {
        storeUser(data.user);
      }
      
      // Store session if provided (some APIs don't return a session on signup)
      if (data.session && data.session.access_token && data.session.refresh_token) {
        storeAuthSession(data.session);
      }
      
      
      
      sendResponse({ 
        success: true, 
        user: data.user
      });
    })
    .catch(error => {
      console.error("❌ Error in signup:", error);
      sendResponse({ 
        success: false, 
        error: error.message || "Failed to create account" 
      });
    });
    
    return true; // Keep channel open for async response
  }
  
  // In src/extension/background/background.js
  function googleSignIn(sendResponse) {
    
    const manifest = chrome.runtime.getManifest();
    const redirectUri = `https://${chrome.runtime.id}.chromiumapp.org`;
    
    // Ensure required configuration is present
    if (!manifest.oauth2 || !manifest.oauth2.client_id) {
      console.error("❌ Missing Google OAuth client ID in manifest");
      sendResponse({ 
        success: false, 
        error: "Google OAuth is not properly configured"
      });
      return true;
    }
    
    const authUrl = new URL('https://accounts.google.com/o/oauth2/auth');
    authUrl.searchParams.set('client_id', manifest.oauth2.client_id);
    authUrl.searchParams.set('response_type', 'id_token');
    authUrl.searchParams.set('access_type', 'offline');
    authUrl.searchParams.set('redirect_uri', redirectUri);
    authUrl.searchParams.set('scope', (manifest.oauth2.scopes || ['email', 'profile']).join(' '));
    authUrl.searchParams.set('prompt', 'consent');
  
  
    chrome.identity.launchWebAuthFlow({ 
      url: authUrl.href, 
      interactive: true 
    }, async (redirectedUrl) => {
      if (chrome.runtime.lastError) {
        console.error("❌ Google Sign-In failed:", chrome.runtime.lastError);
        sendResponse({ 
          success: false, 
          error: chrome.runtime.lastError.message || "Google authentication was canceled" 
        });
        return;
      }
  
      if (!redirectedUrl) {
        console.error("❌ No redirect URL received");
        sendResponse({ 
          success: false, 
          error: "No authentication data received from Google" 
        });
        return;
      }
  
      try {
        const url = new URL(redirectedUrl);
        const params = new URLSearchParams(url.hash.replace("#", "?"));
        const idToken = params.get("id_token");
  
        if (!idToken) {
          console.error("❌ No id_token in redirect URL");
          sendResponse({ 
            success: false, 
            error: "Google authentication didn't return an ID token" 
          });
          return;
        }
  
  
        // Use environment variable for the API endpoint
        const apiUrl = process.env.VITE_API_URL;
        const response = await fetch(`${apiUrl}/auth/sign_in_with_google`, {
          method: "POST",
          headers: { 
            "Content-Type": "application/json",
            "Origin": chrome.runtime.getURL('') 
          },
          body: JSON.stringify({ 
            id_token: idToken
          }),
          credentials: 'include'
        });
  
        const data = await response.json();
        
        if (!response.ok) {
          console.error("❌ Backend authentication failed:", data);
          sendResponse({ 
            success: false, 
            error: data.detail || data.error || "Backend authentication failed" 
          });
          return;
        }
        
        // Validate required data
        if (!data.session || !data.session.access_token || !data.session.refresh_token) {
          console.error("❌ Invalid response from Google auth endpoint (missing session data):", data);
          sendResponse({ 
            success: false, 
            error: "Server returned invalid authentication data" 
          });
          return;
        }
        
        
        // Store authentication data
        storeAuthSession(data.session);
        
        if (data.user) {
          storeUser(data.user);
        }

        
        sendResponse({ 
          success: true, 
          user: data.user, 
          session: data.session
        });
      } catch (error) {
        console.error("❌ Error processing Google authentication:", error);
        sendResponse({ 
          success: false, 
          error: error.message || "Failed to process Google authentication" 
        });
      }
    });
    
    return true; // Keep channel open for async response
  }
  
  /**
   * Store user data
   */
  function storeUser(user) {
    if (!user) {
      console.error("❌ Attempted to store undefined/null user");
      return;
    }
  
    chrome.storage.local.set({ user: user }, () => {
      if (chrome.runtime.lastError) {
        console.error("❌ Error storing user data:", chrome.runtime.lastError);
      } 
    });
  }
  
  
  function storeUserId(userId) {
    if (!userId) {
      console.error("❌ Attempted to store empty user ID");
      return;
    }
  
    chrome.storage.local.set({ userId: userId }, () => {
      if (chrome.runtime.lastError) {
        console.error("❌ Error storing user ID:", chrome.runtime.lastError);
      }
    });
  }



/**
 * Store authentication session
 */
function storeAuthSession(session) {
  if (!session) {
    console.error("❌ Attempted to store undefined/null session");
    return;
  }

  if (!session.access_token || !session.refresh_token) {
    console.error("❌ Incomplete session data:", session);
    return;
  }

  
  chrome.storage.local.set({
    access_token: session.access_token,
    refresh_token: session.refresh_token,
    token_expires_at: session.expires_at,
  }, () => {
    if (chrome.runtime.lastError) {
      console.error("❌ Error storing auth session:", chrome.runtime.lastError);
    }
  });
}


/* ==========================================
 🔹 AUTH TOKEN MANAGEMENT
========================================== */
function sendAuthToken(sendResponse) {
    chrome.storage.local.get(["access_token", "refresh_token", "token_expires_at", "user"], (result) => {
      const now = Math.floor(Date.now() / 1000);
  
      // Check if we have a valid token
      if (result.access_token && result.token_expires_at && result.token_expires_at > now) {
        sendResponse({ success: true, token: result.access_token });
        return;
      }
      
      // Check if we have a refresh token to attempt refresh
      if (result.refresh_token) {
        refreshAndSendToken(sendResponse);
        return;
      }
      
      // No valid tokens available - check if we have a user saved
      if (result.user && result.user.id) {
        // Here we'd ideally implement a silent sign-in mechanism
        // For now, just notify the user they need to re-authenticate
        sendResponse({ 
          success: false, 
          error: "Session expired", 
          errorCode: "SESSION_EXPIRED", 
          needsReauth: true 
        });
        return;
      }
      
      // No user data and no tokens - completely unauthenticated
      console.error("❌ No authentication data found");
      sendResponse({ 
        success: false, 
        error: "Not authenticated", 
        errorCode: "NOT_AUTHENTICATED", 
        needsReauth: true 
      });
    });
    return true; // Keep channel open for async response
  }
  
  function refreshAndSendToken(sendResponse) {
    chrome.storage.local.get(["refresh_token", "user"], async (result) => {
      if (!result.refresh_token) {
        console.error("❌ No refresh token available");
        
        // Check if we have user data to give helpful error
        if (result.user && result.user.id) {
          sendResponse({ 
            success: false, 
            error: chrome.i18n.getMessage('sessionExpired', undefined, 'Session expired. Please sign in again.'),
            errorCode: "REFRESH_TOKEN_MISSING",
            needsReauth: true
          });
        } else {
          sendResponse({ 
            success: false, 
            error: chrome.i18n.getMessage('notAuthenticated', undefined, 'Not authenticated. Please sign in.'),
            errorCode: "NOT_AUTHENTICATED",
            needsReauth: true
          });
        }
        return;
      }
      
      try {
        const response = await fetch(`${process.env.VITE_API_URL}/auth/refresh_token`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh_token: result.refresh_token }),
        });
        
        if (!response.ok) {
          console.error("❌ Token refresh failed:", await response.text());
          // If refresh fails with 401/403, the refresh token is likely invalid
          if (response.status === 401 || response.status === 403) {
            // Clear invalid tokens
            chrome.storage.local.remove(["access_token", "refresh_token", "token_expires_at"]);
            
            sendResponse({ 
              success: false, 
              error: chrome.i18n.getMessage('sessionExpired', undefined, 'Session expired. Please sign in again.'),
              errorCode: "INVALID_REFRESH_TOKEN",
              needsReauth: true
            });
          } else {
            sendResponse({ 
              success: false, 
              error: chrome.i18n.getMessage('refreshFailed', undefined, 'Failed to refresh token. Please try again.'),
              errorCode: "REFRESH_FAILED"
            });
          }
          return;
        }
  
        const data = await response.json();
        
        if (!data.session || !data.session.access_token) {
          console.error("❌ Invalid response from refresh endpoint:", data);
          sendResponse({ 
            success: false, 
            error: "Invalid response from server", 
            errorCode: "INVALID_RESPONSE"
          });
          return;
        }
        
        // Store the new session data
        storeAuthSession(data.session);
        sendResponse({ success: true, token: data.session.access_token });
      } catch (error) {
        console.error("❌ Error refreshing access token:", error);
        sendResponse({ 
          success: false, 
          error: chrome.i18n.getMessage('networkError', undefined, 'Network error while refreshing token'), 
          errorCode: "NETWORK_ERROR"
        });
      }
    });
    return true; // Keep channel open for async response
  }
  
  
  
  /**
   * Clear authentication data - useful for sign out or when tokens become invalid
   */
  function clearAuthData(callback) {
    chrome.storage.local.remove(
      ["access_token", "refresh_token", "token_expires_at"], 
      () => {
        if (callback) callback();
      }
    );
  }
  

/* ==========================================
 🔹 DEV RELOAD
========================================== */

chrome.storage.onChanged.addListener((changes, namespace) => {
    if (namespace === 'local' && changes.devReloadTimestamp) {
        // Reload all extension pages
        chrome.runtime.reload();
    }
});
