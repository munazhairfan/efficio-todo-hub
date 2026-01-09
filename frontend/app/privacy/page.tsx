export default function PrivacyPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">Privacy Policy</h1>

      <div className="prose prose-lg">
        <p className="mb-4">
          Your privacy is important to us. This Privacy Policy explains how we collect, use, and protect your personal information when you use our Efficio Todo Hub application.
        </p>

        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-3">Information We Collect</h2>
          <p>
            We collect information you provide directly to us, such as when you create an account, use our services, or communicate with us. This includes:
          </p>
          <ul className="list-disc pl-6 mt-2">
            <li>Email address and name when you create an account</li>
            <li>Todo items and related information you create using our service</li>
            <li>Usage data when you interact with our application</li>
          </ul>
        </section>

        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-3">How We Use Your Information</h2>
          <p>
            We use the information we collect to:
          </p>
          <ul className="list-disc pl-6 mt-2">
            <li>Provide, maintain, and improve our services</li>
            <li>Communicate with you about our services</li>
            <li>Protect against fraudulent or unauthorized activity</li>
          </ul>
        </section>

        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-3">Data Security</h2>
          <p>
            We implement appropriate security measures to protect against unauthorized access, alteration, disclosure, or destruction of your personal information.
          </p>
        </section>

        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-3">Your Rights</h2>
          <p>
            You have the right to access, update, or delete your personal information at any time. You can do this by contacting us or using the account management features in our application.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold mb-3">Contact Us</h2>
          <p>
            If you have questions about this Privacy Policy, please contact us at [your contact email].
          </p>
        </section>
      </div>
    </div>
  );
}