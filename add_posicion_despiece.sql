-- =====================================================================
-- Columnas para ubicar cada repuesto sobre la imagen de despiece (%)
-- Ejecutar una sola vez en el SQL Editor de Supabase
-- =====================================================================

alter table repuestos
    add column if not exists pos_x numeric(5,2), -- posición horizontal en % (0-100) sobre la imagen del componente
    add column if not exists pos_y numeric(5,2); -- posición vertical en % (0-100) sobre la imagen del componente
