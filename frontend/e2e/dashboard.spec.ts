import { test, expect } from '@playwright/test';

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display dashboard page', async ({ page }) => {
    await expect(page.locator('h2')).toContainText('Dashboard');
  });

  test('should display KPI cards', async ({ page }) => {
    await expect(page.locator('text=Total Vehicles')).toBeVisible();
    await expect(page.locator('text=Total Drivers')).toBeVisible();
    await expect(page.locator('text=Active Trips')).toBeVisible();
    await expect(page.locator('text=Fleet Utilization')).toBeVisible();
  });

  test('should navigate to vehicles page', async ({ page }) => {
    await page.click('text=Vehicles');
    await expect(page).toHaveURL('/vehicles');
    await expect(page.locator('h2')).toContainText('Vehicles');
  });

  test('should navigate to drivers page', async ({ page }) => {
    await page.click('text=Drivers');
    await expect(page).toHaveURL('/drivers');
    await expect(page.locator('h2')).toContainText('Drivers');
  });

  test('should navigate to trips page', async ({ page }) => {
    await page.click('text=Trips');
    await expect(page).toHaveURL('/trips');
    await expect(page.locator('h2')).toContainText('Trips');
  });

  test('should navigate to tracking page', async ({ page }) => {
    await page.click('text=Tracking');
    await expect(page).toHaveURL('/tracking');
    await expect(page.locator('h2')).toContainText('Live Tracking');
  });

  test('should navigate to AI assistant page', async ({ page }) => {
    await page.click('text=AI Assistant');
    await expect(page).toHaveURL('/assistant');
    await expect(page.locator('h2')).toContainText('AI Assistant');
  });

  test('should navigate to ML predictions page', async ({ page }) => {
    await page.click('text=ML Predictions');
    await expect(page).toHaveURL('/predictions');
    await expect(page.locator('h2')).toContainText('ML Predictions');
  });

  test('should navigate to analytics page', async ({ page }) => {
    await page.click('text=Analytics');
    await expect(page).toHaveURL('/analytics');
    await expect(page.locator('h2')).toContainText('Analytics');
  });
});
