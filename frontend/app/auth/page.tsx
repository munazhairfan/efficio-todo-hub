'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useAuth } from '@/components/auth/AuthProvider';
import { Eye, EyeOff } from 'lucide-react';

export default function AuthPage() {
  const { signup, signin } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const router = useRouter();

  // Determine the default tab based on URL query parameter
  const getDefaultTab = () => {
    if (typeof window !== 'undefined') {
      const urlParams = new URLSearchParams(window.location.search);
      const tabParam = urlParams.get('tab');
      if (tabParam === 'signup') {
        return 'signup';
      }
    }
    return 'signin'; // default to signin
  };

  const [activeTab, setActiveTab] = useState(getDefaultTab());

  // Signin state
  const [signinEmail, setSigninEmail] = useState('');
  const [signinPassword, setSigninPassword] = useState('');
  const [signinError, setSigninError] = useState('');
  const [signinLoading, setSigninLoading] = useState(false);

  // Signup state
  const [signupName, setSignupName] = useState('');
  const [signupEmail, setSignupEmail] = useState('');
  const [signupPassword, setSignupPassword] = useState('');
  const [signupConfirmPassword, setSignupConfirmPassword] = useState('');
  const [signupError, setSignupError] = useState('');
  const [signupLoading, setSignupLoading] = useState(false);

  const handleSignin = async (e: React.FormEvent) => {
    e.preventDefault();
    setSigninError('');
    setSigninLoading(true); // Set loading state
    console.log('Starting signin process...');

    try {
      console.log('Calling signin function...');
      const result = await signin(signinEmail, signinPassword);
      console.log('Signin successful, result:', result);
      console.log('Navigating to dashboard...');

      // Wait a brief moment to ensure token is properly stored in both localStorage and cookies
      await new Promise(resolve => setTimeout(resolve, 100));

      // Use Next.js router for navigation to maintain React state
      router.push('/dashboard');

      console.log('Navigation completed');
    } catch (error) {
      setSigninError('Invalid email or password');
      console.error('Signin error:', error);
    } finally {
      setSigninLoading(false); // Always reset loading state
      console.log('Signin loading state reset');
    }
  };

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setSignupError('');
    setSignupLoading(true); // Set loading state
    console.log('Starting signup process...');

    if (signupPassword !== signupConfirmPassword) {
      setSignupError('Passwords do not match');
      setSignupLoading(false); // Reset loading state
      console.log('Password mismatch error');
      return;
    }

    if (signupPassword.length < 8) {
      setSignupError('Password must be at least 8 characters');
      setSignupLoading(false); // Reset loading state
      console.log('Password length error');
      return;
    }

    try {
      console.log('Calling signup function...');
      const result = await signup(signupEmail, signupPassword, signupName);
      console.log('Signup successful, result:', result);
      console.log('Navigating to dashboard...');

      // Wait a brief moment to ensure token is properly stored in both localStorage and cookies
      await new Promise(resolve => setTimeout(resolve, 100));

      // Use Next.js router for navigation to maintain React state
      router.push('/dashboard');

      console.log('Navigation completed');
    } catch (error) {
      setSignupError('Failed to create account. Email may already be in use.');
      console.error('Signup error:', error);
      console.error('Full error:', error);
    } finally {
      setSignupLoading(false); // Always reset loading state
      console.log('Signup loading state reset');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-mint-julep to-confetti p-4">
      <div className="w-full max-w-md">
        <Card className="border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] rounded-2xl overflow-hidden">
          <CardHeader className="text-center pb-4">
            <CardTitle className="text-3xl font-black text-merlot">Welcome to Efficio</CardTitle>
            <CardDescription className="text-lg text-mojo">
              Get things done with fun!
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="grid w-full grid-cols-2 h-14 mb-6">
                <TabsTrigger
                  value="signin"
                  className="text-lg font-bold data-[state=active]:bg-mojo data-[state=active]:text-white rounded-lg"
                >
                  Sign In
                </TabsTrigger>
                <TabsTrigger
                  value="signup"
                  className="text-lg font-bold data-[state=active]:bg-mojo data-[state=active]:text-white rounded-lg"
                >
                  Sign Up
                </TabsTrigger>
              </TabsList>

              <TabsContent value="signin" className="space-y-4">
                <form onSubmit={handleSignin} className="space-y-4">
                  {signinError && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                      <span className="block sm:inline">{signinError}</span>
                    </div>
                  )}

                  <div className="space-y-2">
                    <Label htmlFor="signin-email" className="text-merlot font-bold">Email</Label>
                    <Input
                      id="signin-email"
                      type="email"
                      placeholder="your@email.com"
                      value={signinEmail}
                      onChange={(e) => setSigninEmail(e.target.value)}
                      className="h-12 border-2 border-merlot rounded-lg px-4 text-lg"
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="signin-password" className="text-merlot font-bold">Password</Label>
                    <div className="relative">
                      <Input
                        id="signin-password"
                        type={showPassword ? "text" : "password"}
                        placeholder="••••••••"
                        value={signinPassword}
                        onChange={(e) => setSigninPassword(e.target.value)}
                        className="h-12 border-2 border-merlot rounded-lg px-4 text-lg pr-12"
                        required
                      />
                      <button
                        type="button"
                        className="absolute inset-y-0 right-0 pr-3 flex items-center text-merlot"
                        onClick={() => setShowPassword(!showPassword)}
                      >
                        {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                      </button>
                    </div>
                  </div>

                  <Button
                    type="submit"
                    disabled={signinLoading}
                    className="w-full h-12 bg-mojo hover:bg-merlot text-white font-black text-lg border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all rounded-xl disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {signinLoading ? (
                      <div className="flex items-center">
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Signing In...
                      </div>
                    ) : (
                      "Sign In"
                    )}
                  </Button>
                </form>
              </TabsContent>

              <TabsContent value="signup" className="space-y-4">
                <form onSubmit={handleSignup} className="space-y-4">
                  {signupError && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                      <span className="block sm:inline">{signupError}</span>
                    </div>
                  )}

                  <div className="space-y-2">
                    <Label htmlFor="signup-name" className="text-merlot font-bold">Full Name</Label>
                    <Input
                      id="signup-name"
                      type="text"
                      placeholder="John Doe"
                      value={signupName}
                      onChange={(e) => setSignupName(e.target.value)}
                      className="h-12 border-2 border-merlot rounded-lg px-4 text-lg"
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="signup-email" className="text-merlot font-bold">Email</Label>
                    <Input
                      id="signup-email"
                      type="email"
                      placeholder="your@email.com"
                      value={signupEmail}
                      onChange={(e) => setSignupEmail(e.target.value)}
                      className="h-12 border-2 border-merlot rounded-lg px-4 text-lg"
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="signup-password" className="text-merlot font-bold">Password</Label>
                    <div className="relative">
                      <Input
                        id="signup-password"
                        type={showPassword ? "text" : "password"}
                        placeholder="••••••••"
                        value={signupPassword}
                        onChange={(e) => setSignupPassword(e.target.value)}
                        className="h-12 border-2 border-merlot rounded-lg px-4 text-lg pr-12"
                        required
                      />
                      <button
                        type="button"
                        className="absolute inset-y-0 right-0 pr-3 flex items-center text-merlot"
                        onClick={() => setShowPassword(!showPassword)}
                      >
                        {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                      </button>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="signup-confirm-password" className="text-merlot font-bold">Confirm Password</Label>
                    <div className="relative">
                      <Input
                        id="signup-confirm-password"
                        type={showConfirmPassword ? "text" : "password"}
                        placeholder="••••••••"
                        value={signupConfirmPassword}
                        onChange={(e) => setSignupConfirmPassword(e.target.value)}
                        className="h-12 border-2 border-merlot rounded-lg px-4 text-lg pr-12"
                        required
                      />
                      <button
                        type="button"
                        className="absolute inset-y-0 right-0 pr-3 flex items-center text-merlot"
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      >
                        {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                      </button>
                    </div>
                  </div>

                  <Button
                    type="submit"
                    disabled={signupLoading}
                    className="w-full h-12 bg-mojo hover:bg-merlot text-white font-black text-lg border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all rounded-xl disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {signupLoading ? (
                      <div className="flex items-center">
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Creating...
                      </div>
                    ) : (
                      "Create Account"
                    )}
                  </Button>
                </form>
              </TabsContent>
            </Tabs>
          </CardContent>
          <CardFooter className="flex justify-center">
            <p className="text-sm text-merlot">
              By signing in or creating an account, you agree to our{' '}
              <Link href="/terms" className="underline hover:text-mojo">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link href="/privacy" className="underline hover:text-mojo">
                Privacy Policy
              </Link>
              .
            </p>
          </CardFooter>
        </Card>

        <div className="mt-6 text-center">
          <Link href="/" className="text-merlot hover:text-mojo font-bold underline">
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}