with source as (
    select * from {{ source('raw', 'raw_ai4i2020') }}
),

renamed as (
    select
        udi::integer                        as udi,
        product_id                          as product_id,
        type                                as product_type,
        air_temperature_k::numeric          as air_temperature_k,
        process_temperature_k::numeric      as process_temperature_k,
        rotational_speed_rpm::integer       as rotational_speed_rpm,
        torque_nm::numeric                  as torque_nm,
        tool_wear_min::integer              as tool_wear_min,
        machine_failure::integer            as machine_failure,
        twf::integer                        as twf,
        hdf::integer                        as hdf,
        pwf::integer                        as pwf,
        osf::integer                        as osf,
        rnf::integer                        as rnf
    from source
)

select * from renamed
