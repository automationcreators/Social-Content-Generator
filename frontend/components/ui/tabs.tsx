import React from 'react'
import * as TabsPrimitive from '@radix-ui/react-tabs'

const Tabs = TabsPrimitive.Root
const TabsList = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={`inline-flex h-10 items-center justify-center rounded-md bg-gray-100 p-1 ${className}`} {...props} />
  )
)
const TabsTrigger = React.forwardRef<HTMLButtonElement, React.HTMLAttributes<HTMLButtonElement> & { value: string }>(
  ({ className, ...props }, ref) => (
    <button ref={ref} className={`inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-white data-[state=active]:text-gray-900 data-[state=active]:shadow-sm ${className}`} {...props} />
  )
)
const TabsContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & { value: string }>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={`mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ${className}`} {...props} />
  )
)

export { Tabs, TabsList, TabsTrigger, TabsContent }
