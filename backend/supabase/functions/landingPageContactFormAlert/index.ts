// Follow this setup guide to integrate the Deno language server with your editor:
// https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.

// Setup type definitions for built-in Supabase Runtime APIs
import "jsr:@supabase/functions-js/edge-runtime.d.ts"

console.log("Hello from Functions!")

Deno.serve(async (req) => {
  try {
    const { record } = await req.json()

    const SENDGRID_API_KEY = Deno.env.get("SENDGRID_API_KEY")!
    const FROM_EMAIL = "no-reply@jayd.ai"
    const CONTACT_EMAIL = "contact@jayd.ai"
    
    // Check if this is a Chrome extension instructions request
    if (record.subject === "Chrome extension instructions request") {
      // Send engaging email to the user who requested the instructions
      const userEmailResponse = await sendEmail({
        to: record.email,
        from: FROM_EMAIL,
        subject: "✨ Téléchargez l'extension Jaydai pour Google Chrome",
        content: getExtensionInstructionsEmailContent()
      }, SENDGRID_API_KEY)
      
      if (!userEmailResponse.ok) {
        const errorText = await userEmailResponse.text()
        console.error("Erreur d'envoi SendGrid (email utilisateur):", errorText)
        return new Response("Erreur SendGrid lors de l'envoi à l'utilisateur", { status: 500 })
      }
      
      return new Response("Email d'instructions envoyé à l'utilisateur", { status: 200 })
    } else {
      // For all other cases, send notification to contact@jayd.ai
      const contactEmailResponse = await sendEmail({
        to: CONTACT_EMAIL,
        from: FROM_EMAIL,
        subject: "🆕 Nouveau message depuis le formulaire de contact",
        content: getContactFormNotificationContent(record)
      }, SENDGRID_API_KEY)
      
      if (!contactEmailResponse.ok) {
        const errorText = await contactEmailResponse.text()
        console.error("Erreur d'envoi SendGrid (email notification):", errorText)
        return new Response("Erreur SendGrid lors de l'envoi de la notification", { status: 500 })
      }
      
      return new Response("Notification de contact envoyée", { status: 200 })
    }
  } catch (error) {
    console.error("Erreur dans la fonction Edge:", error)
    return new Response(`Erreur: ${error.message}`, { status: 500 })
  }
})

// Helper function to send email via SendGrid
async function sendEmail({ to, from, subject, content }, apiKey) {
  return await fetch("https://api.sendgrid.com/v3/mail/send", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      personalizations: [{ to: [{ email: to }] }],
      from: { email: from, name: "Jaydai" },
      subject: subject,
      content: [{ type: "text/html", value: content }],
    }),
  })
}

// Email content for Chrome extension instructions
function getExtensionInstructionsEmailContent() {
  
  return `
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <title>Jaydai - Téléchargez l'extension Chrome</title>
  <!--[if mso]>
  <style type="text/css">
    body, table, td {font-family: Arial, Helvetica, sans-serif !important;}
    .button {background-color: #676ADD !important; padding: 4px 12px !important; border-radius: 8px !important;}
  </style>
  <![endif]-->
  <style>
    :root {
      color-scheme: light dark;
      supported-color-schemes: light dark;
    }
    
    @media (prefers-color-scheme: dark) {
      .dark-invert { filter: brightness(0.8) contrast(1.2); }
      .logo-bg { background-color: #252729 !important; }
      .body-bg { background-color: #1a1b21 !important; }
      .content-bg { background-color: #1a1b21 !important; }
      .title { color: #9b9bf9 !important; }
      .text { color: #eaeaea !important; }
      .warning-bg { background-color: rgba(255, 182, 72, 0.1) !important; border: 1px solid rgba(255, 182, 72, 0.2) !important; }
      .warning-text { color: #ffb648 !important; }
      .tutorial-bg { background-color: #252729 !important; border: 1px solid #333438 !important; }
      .tutorial-text { color: #9b9bf9 !important; }
      .divider { background-color: #333438 !important; }
      .footer-text { color: #a1a1aa !important; }
      .footer-link { color: #a1a1aa !important; border-bottom: 1px dotted #a1a1aa !important; }
    }
  </style>
</head>
<body style="margin: 0; padding: 0; font-family: 'Roboto', Arial, sans-serif; color: #1e293b; background-color: #f8fafc;" class="body-bg">
  <!-- Email container -->
  <div style="margin: 0 auto; padding: 10px; max-width: 100%;">
    <!-- Main Content -->
    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);" class="content-bg">
      <tr>
        <td>
          <!-- Header -->
          <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background: #030615;">
            <tr>
              <td align="center" style="padding: 40px 20px;">
                <img src="https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images//jaydai-extension-logo.png" alt="Logo Jaydai" width="100" style="display: block; background-color: white; border-radius: 12px; padding: 10px; max-width: 100px; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);" class="logo-bg dark-invert">
              </td>
            </tr>
          </table>
          
          <!-- Content -->
          <table cellpadding="0" cellspacing="0" border="0" width="100%">
            <tr>
              <td style="padding: 35px 20px 30px;">
                <!-- Title -->
                <h1 style="font-family: 'Poppins', Arial, sans-serif; font-size: 28px; font-weight: 700; color: #676ADD; margin: 0 0 25px; line-height: 1.3; text-align: center;" class="title">Merci pour ton intérêt pour Jaydai !</h1>
                
                <!-- Desktop Warning Box -->
                <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin: 0 auto 25px; width: 100%;">
                  <tr>
                    <td align="center" style="background-color: rgba(255, 182, 72, 0.1); border-radius: 12px; padding: 12px 15px; border: 1px solid rgba(255, 182, 72, 0.2);" class="warning-bg">
                      <p style="margin: 0; font-family: 'Roboto', Arial, sans-serif; font-size: 15px; color: #b45309; font-weight: 500; text-align: center;" class="warning-text">
                        ⚠️ L'extension Jaydai ne peut être téléchargée que sur un ordinateur avec Google Chrome
                      </p>
                    </td>
                  </tr>
                </table>
                
                <!-- Download section -->
                <p style="margin-bottom: 25px; font-size: 16px; line-height: 1.6; color: #475569; text-align: center;" class="text">
                  Télécharge l'extension dès maintenant sur le Chrome Web Store :
                </p>
                
                <!-- Download Button -->
                <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin: 15px auto 30px; width: 100%; max-width: 280px;">
                  <tr>
                    <td align="center" style="background-color: #676ADD; border-radius: 12px; padding: 0;">
                      <a href="https://chromewebstore.google.com/detail/jaydai-chrome-extension/enfcjmbdbldomiobfndablekgdkmcipd" style="display: block; padding: 16px 10px; font-family: 'Poppins', Arial, sans-serif; font-size: 17px; color: #ffffff; text-decoration: none; font-weight: 600; letter-spacing: 0.3px; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">
                        Télécharger Jaydai ⚡️
                      </a>
                    </td>
                  </tr>
                </table>
                
                <!-- Tutorial section -->
                <p style="margin: 30px 0 15px; font-size: 16px; line-height: 1.6; color: #475569; text-align: center;" class="text">
                  Besoin d'aide pour l'installation ? Regarde notre tutoriel rapide :
                </p>
                
                <!-- Tutorial Link -->
                <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin: 0 auto 30px; width: 100%; max-width: 280px;">
                  <tr>
                    <td align="center" style="background-color: rgba(103, 106, 221, 0.1); border-radius: 12px; border: 1px solid rgba(103, 106, 221, 0.15);" class="tutorial-bg">
                      <a href="https://www.youtube.com/watch?v=vUAbWXIa2EA" style="display: block; padding: 12px 10px; font-family: 'Roboto', Arial, sans-serif; font-size: 16px; color: #676ADD; text-decoration: none; font-weight: 600; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;" class="tutorial-text">
                        Voir la vidéo d'explication 📺
                      </a>
                    </td>
                  </tr>
                </table>
                
                <!-- Closing -->
                <p style="margin-top: 30px; text-align: center; font-size: 16px; line-height: 1.6; color: #475569;" class="text">
                  À très vite sur Jaydai 🚀
                </p>
              </td>
            </tr>
          </table>
          
          <!-- Divider -->
          <table cellpadding="0" cellspacing="0" border="0" width="100%">
            <tr>
              <td style="padding: 0 30px;">
                <div style="height: 1px; background-color: #e2e8f0; margin: 0;" class="divider"></div>
              </td>
            </tr>
          </table>
          
          <!-- Footer -->
          <table cellpadding="0" cellspacing="0" border="0" width="100%">
            <tr>
              <td style="padding: 30px 20px 40px; text-align: center; color: #94a3b8; font-size: 13px;" class="footer-text">
                © 2025 Jaydai. Tous droits réservés.<br/>
                <a href="https://jayd.ai/privacy" style="color: #94a3b8; text-decoration: none; border-bottom: 1px dotted #94a3b8; padding-bottom: 1px;" class="footer-link">Politique de confidentialité</a> &nbsp;|&nbsp; 
                <a href="https://www.jayd.ai/fr/terms-of-service" style="color: #94a3b8; text-decoration: none; border-bottom: 1px dotted #94a3b8; padding-bottom: 1px;" class="footer-link">Conditions d'utilisation</a>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </div>
</body>
</html>

  `
}

// Email content for contact form notification
function getContactFormNotificationContent(record) {
  return `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
      <h1 style="color: #4a6cf7;">Nouveau message du formulaire de contact</h1>
      
      <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 20px;">
        <p><strong>Nom :</strong> ${record.name || 'Non spécifié'}</p>
        <p><strong>Email :</strong> ${record.email || 'Non spécifié'}</p>
        <p><strong>Objet :</strong> ${record.subject || 'Non spécifié'}</p>
        <hr style="border: none; border-top: 1px solid #ddd; margin: 15px 0;">
        <p><strong>Message :</strong></p>
        <p style="white-space: pre-line;">${record.message || 'Aucun message'}</p>
      </div>
      
      <p style="margin-top: 20px; color: #666; font-size: 12px;">
        Ce message a été envoyé via le formulaire de contact du site Jaydai le ${new Date().toLocaleString('fr-FR', {
          day: '2-digit',
          month: '2-digit', 
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })}.
      </p>
    </div>
  `
}

/* To invoke locally:

  1. Run `supabase start` (see: https://supabase.com/docs/reference/cli/supabase-start)
  2. Make an HTTP request:

  curl -i --location --request POST 'http://127.0.0.1:54321/functions/v1/landingPageContactFormAlert' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0' \
    --header 'Content-Type: application/json' \
    --data '{"record":{"name":"Test User","email":"test@example.com","subject":"Chrome extension instructions request","message":"Please send me instructions."}}'

*/