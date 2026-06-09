with staging as (
    select * from {{ ref('stg_ai4i2020') }}
),

enriched as (
    select
        -- Identificadores
        udi,
        product_id,
        product_type,

        -- Sensores originales
        air_temperature_k,
        process_temperature_k,
        rotational_speed_rpm,
        torque_nm,
        tool_wear_min,

        -- Variables derivadas de negocio
        round((process_temperature_k - air_temperature_k)::numeric, 2)
            as temperature_delta_k,

        round((torque_nm * rotational_speed_rpm / 9550.0)::numeric, 4)
            as power_kw,

        case
            when tool_wear_min < 100 then 'low'
            when tool_wear_min between 100 and 200 then 'medium'
            else 'high'
        end as tool_wear_category,

        -- Fallas
        machine_failure,
        twf,
        hdf,
        pwf,
        osf,
        rnf,

        -- Indicador de falla multiple
        (twf + hdf + pwf + osf + rnf) as total_failure_modes

    from staging
)

select * from enriched
