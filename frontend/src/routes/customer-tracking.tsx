import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/customer-tracking')({
  component: CustomerTrackingRedirect,
})

function CustomerTrackingRedirect() {
  // Redirect to the standalone HTML page
  window.location.href = '/customer-tracking.html'
  return null
}