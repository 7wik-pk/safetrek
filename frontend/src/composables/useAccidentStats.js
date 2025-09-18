// composables/useAccidentStats.js
export async function fetchAccidentStats({
  filter_area_level,
  filter_area_name,
  group_by_area_level,
  date_from,
  date_to,
  order_by = 'count',
  order_dir = 'desc',
  limit = 10,
  API = import.meta.env.VITE_API_BASE ?? '/api',
}) {
  const body = {
    filter_area_level,
    filter_area_name,
    group_by_area_level,
    date_from: date_from || null,
    date_to: date_to || null,
    order_by,
    order_dir,
    limit,
  }

  const res = await fetch(`${API}/accident_stats`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    const txt = await res.text().catch(() => '')
    throw new Error(`accident_stats ${res.status} ${txt}`)
  }

  return await res.json()
}
