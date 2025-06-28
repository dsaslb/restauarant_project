import { Sidebar } from "@/components/ui/Sidebar";

export default function AppLayout({ children }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-8">{children}</main>
    </div>
  );
} 