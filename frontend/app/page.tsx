'use client';

import { Button } from "@/components/ui/button";
import { Navbar } from "@/components/navbar";
import { FeatureCard } from "@/components/feature-card";
import { SectionDivider } from "@/components/section-divider";

export default function LandingPage() {
  return (
    <main className="min-h-screen font-sans selection:bg-mojo selection:text-white overflow-x-hidden">
      {/* Navbar */}
      <Navbar />

      {/* Hero Section */}
      <section className="relative min-h-175 flex items-center justify-center bg-dobger-blue px-4 pt-24">
        <div className="max-w-6xl mx-auto grid lg:grid-cols-2 gap-12 items-center z-20 py-20">
          <div className="space-y-8 animate-in fade-in slide-in-from-left duration-1000">
            <h1 className="text-6xl md:text-8xl font-black text-paris-daisy leading-[1.1] tracking-tight">
              Get Things <span className="text-code-gray">Done</span> with Fun!
            </h1>
            <p className="text-xl md:text-2xl text-paris-daisy/80 font-semibold max-w-xl leading-relaxed">
              The world's most cartoonish productivity tool. Organize your life with a smile and premium vibes.
            </p>
            <div className="flex flex-wrap gap-6">
              <Button
                size="lg"
                className="h-16 px-10 text-xl font-bold bg-code-gray hover:bg-gray-800 text-white rounded-full border-b-8 border-gray-900 active:border-b-0 active:translate-y-1 transition-all shadow-xl"
                onClick={() => window.location.href = '/auth'}
              >
                Get Started
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="h-16 px-10 text-xl font-bold border-4 border-paris-daisy text-paris-daisy hover:bg-paris-daisy hover:text-black rounded-full transition-all shadow-xl bg-transparent"
                onClick={() => {
                  // Check if user is authenticated and redirect accordingly
                  if (typeof window !== 'undefined') {
                    const token = localStorage.getItem('authToken');
                    if (token) {
                      window.location.href = '/dashboard';
                    } else {
                      window.location.href = '/auth';
                    }
                  }
                }}
              >
                Learn More
              </Button>
            </div>
          </div>
          <div className="hidden lg:block animate-in fade-in duration-1000 delay-300">
            <video
              src="/Notebook.mp4"
              autoPlay
              loop
              muted
              playsInline
              disablePictureInPicture
              disableRemotePlayback
              aria-hidden="true"
              className="w-full"
            />
          </div>
        </div>
      </section>

      {/* SectionDivider between Hero and Features */}
      <SectionDivider fromColor="#12a6e1" toColor="#fff467" />

      {/* Features Section */}
      <section className="relative py-20 bg-paris-daisy px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-20 space-y-4">
            <h2 className="text-5xl md:text-6xl font-black text-code-gray">Awesome Features</h2>
            <div className="w-96 h-3 bg-code-gray mx-auto rounded-full" />
          </div>
          <div className="flex flex-row justify-between items-center content-center gap-10 mx-auto">
            <div className="hidden lg:block animate-in fade-in duration-1000 delay-300">
            <video
              src="/Task.mp4"
              autoPlay
              loop
              muted
              playsInline
              disablePictureInPicture
              disableRemotePlayback
              aria-hidden="true"
              className="w-full"
            />
          </div>
          <div className="grid grid-row-3 gap-10">
            <FeatureCard
              title="Smart Lists"
              description="Automatically organize your tasks based on priority and deadlines with our AI-powered logic."
              icon="cartoon list icon"
            />
            <FeatureCard
              title="Cute Badges"
              description="Earn premium cartoon badges for every milestone you reach. Productivity never felt so rewarding!"
              icon="cartoon gold medal icon"
            />
            <FeatureCard
              title="Team Play"
              description="Collaborate with your team in a fun, shared workspace. Emoji reactions included!"
              icon="cartoon team collaboration icon"
            />
          </div>
          </div>
        </div>
      </section>

      {/* SectionDivider between Features and How It Works */}
      <SectionDivider fromColor="#fff467" toColor="#4b7119" />

      {/* How It Works Section */}
      <section className="relative py-20 bg-dello px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="bg-mint-julep">
              <h2 className="text-8xl font-black text-dello text-center">How It Works?</h2>
            </div>
            <div className="space-y-12 order-1 lg:order-2">
              <div className="space-y-8">
                {[
                  {
                    step: "01",
                    title: "Create Your Account",
                    desc: "Join thousands of happy users in just two clicks.",
                  },
                  { step: "02", title: "Add Your Tasks", desc: "List everything you want to achieve today." },
                  { step: "03", title: "Smash Your Goals", desc: "Check them off and watch the cartoon fireworks!" },
                ].map((item, i) => (
                  <div key={i} className="flex gap-6 items-start">
                    <div className="w-16 h-16 shrink-0 bg-mint-julep rounded-2xl border-4 border-lime-900 flex items-center justify-center text-dello text-2xl font-black shadow-lg">
                      {item.step}
                    </div>
                    <div className="space-y-2">
                      <h4 className="text-2xl font-black text-confetti">{item.title}</h4>
                      <p className="text-lg text-confetti/70 font-medium leading-relaxed">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SectionDivider between How It Works and CTA */}
      <SectionDivider fromColor="#4b7119" toColor="#eaefb4" />

      {/* CTA Section */}
      <section className="relative py-32 bg-mint-julep overflow-hidden px-4">
        <div className="max-w-4xl mx-auto text-center relative z-10 space-y-10">
          <h2 className="text-6xl md:text-7xl font-black text-mojo leading-tight">
            Ready to Boost Your Productivity?
          </h2>
          <p className="text-2xl text-mojo/80 font-bold">Join over 100,000+ happy users today.</p>
          <Button
            size="lg"
            className="h-20 px-16 text-3xl font-black bg-mojo hover:bg-merlot text-white rounded-full border-b-12 border-merlot active:border-b-0 active:translate-y-2 transition-all shadow-2xl"
            onClick={() => window.location.href = '/auth?tab=signup'}
          >
        <div className="absolute opacity-10 pointer-events-none">
          <img src="/cartoon-pattern-background-short.jpg" alt="" className="w-full h-full rounded-full object-cover" />
        </div>
            Sign Up Now!  
          </Button>
        </div>
      </section>

      {/* SectionDivider before Footer */}
      <SectionDivider fromColor="#eaefb4" toColor="#7b1c2f" />

      {/* Footer */}
      <footer className="bg-merlot py-16 px-4 mt-0">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="text-paris-daisy text-4xl font-black italic">EFFICIO.</div>
          <div className="flex gap-8">
            {["About", "Privacy", "Contact", "Twitter"].map((link) => (
              <a key={link} href="#" className="text-paris-daisy font-bold text-lg hover:underline underline-offset-8">
                {link}
              </a>
            ))}
          </div>
          <p className="text-paris-daisy/60 font-medium">© 2026 Efficio. All rights reserved.</p>
        </div>
      </footer>
    </main>
  )
}