'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth/AuthProvider';
import { api } from '@/lib/api';
import { User } from '@/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LogOut } from 'lucide-react';

export default function ProfilePage() {
  const { user: authUser, isAuthenticated, loading: authLoading, signout } = useAuth();
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [updateSuccess, setUpdateSuccess] = useState(false);

  useEffect(() => {
    if (authLoading) {
      return;
    }

    if (!isAuthenticated) {
      router.push('/auth');
      return;
    }

    // Use the auth user data if available, otherwise fetch fresh
    if (authUser) {
      setUser(authUser);
      setName(authUser.name);
      setEmail(authUser.email);
      setLoading(false);
    } else {
      fetchUser();
    }
  }, [isAuthenticated, authLoading, authUser]);

  const fetchUser = async () => {
    try {
      setLoading(true);
      // Use API directly since the user from context might be incomplete
      const response = await api.getUser();
      setUser(response);
      setName(response.name);
      setEmail(response.email);
    } catch (err) {
      setError('Failed to load user profile');
      console.error('Error fetching user:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSignOut = () => {
    signout();
    router.push('/auth');
    router.refresh();
  };

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // For now, we'll just update the local state since we don't have an API endpoint to update user
      // In a real app, you would make an API call to update the user
      setUser(prev => prev ? { ...prev, name, email } : null);
      setIsEditing(false);
      setUpdateSuccess(true);
      setTimeout(() => setUpdateSuccess(false), 3000);
    } catch (err) {
      setError('Failed to update profile');
      console.error('Error updating profile:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-mint-julep to-confetti">
        <p className="text-2xl font-bold text-merlot">Loading profile...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-mint-julep to-confetti">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative max-w-md w-full mx-4" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-mint-julep to-confetti p-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <header className="flex justify-between items-center py-6 mb-8">
          <h1 className="text-4xl font-black text-merlot">Your Profile</h1>
          <Button
            onClick={handleSignOut}
            variant="outline"
            className="border-2 border-merlot text-merlot hover:bg-merlot hover:text-white"
          >
            <LogOut className="mr-2 h-4 w-4" />
            Sign Out
          </Button>
        </header>

        {/* Profile Card */}
        <Card className="border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] rounded-xl">
          <CardHeader>
            <CardTitle className="text-2xl font-black text-merlot">Profile Information</CardTitle>
          </CardHeader>
          <CardContent>
            {isEditing ? (
              <form onSubmit={handleUpdateProfile} className="space-y-6">
                {updateSuccess && (
                  <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
                    <span className="block sm:inline">Profile updated successfully!</span>
                  </div>
                )}

                <div className="space-y-2">
                  <Label htmlFor="name" className="text-merlot font-bold">Full Name</Label>
                  <Input
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="h-12 border-2 border-merlot rounded-lg px-4 text-lg"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email" className="text-merlot font-bold">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="h-12 border-2 border-merlot rounded-lg px-4 text-lg"
                    required
                  />
                </div>

                <div className="flex gap-4">
                  <Button
                    type="submit"
                    className="bg-mojo hover:bg-merlot text-white font-black text-lg border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all rounded-xl"
                  >
                    Save Changes
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => {
                      setIsEditing(false);
                      // Reset to original values
                      setName(user?.name || '');
                      setEmail(user?.email || '');
                    }}
                    className="border-2 border-merlot text-merlot hover:bg-merlot hover:text-white"
                  >
                    Cancel
                  </Button>
                </div>
              </form>
            ) : (
              <div className="space-y-6">
                {updateSuccess && (
                  <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
                    <span className="block sm:inline">Profile updated successfully!</span>
                  </div>
                )}

                <div className="space-y-4">
                  <div>
                    <h3 className="text-sm font-bold text-gray-500 mb-1">Full Name</h3>
                    <p className="text-xl font-semibold text-merlot">{user?.name}</p>
                  </div>

                  <div>
                    <h3 className="text-sm font-bold text-gray-500 mb-1">Email</h3>
                    <p className="text-xl font-semibold text-merlot">{user?.email}</p>
                  </div>

                  <div>
                    <h3 className="text-sm font-bold text-gray-500 mb-1">Member Since</h3>
                    <p className="text-xl font-semibold text-merlot">
                      {user ? new Date(user.createdAt).toLocaleDateString() : ''}
                    </p>
                  </div>
                </div>

                <Button
                  onClick={() => setIsEditing(true)}
                  className="w-full bg-mojo hover:bg-merlot text-white font-black text-lg border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all rounded-xl"
                >
                  Edit Profile
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Account Actions */}
        <Card className="border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] rounded-xl mt-8">
          <CardHeader>
            <CardTitle className="text-2xl font-black text-merlot">Account Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Button
                onClick={handleSignOut}
                variant="outline"
                className="w-full border-2 border-red-500 text-red-500 hover:bg-red-500 hover:text-white"
              >
                <LogOut className="mr-2 h-4 w-4" />
                Sign Out
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}