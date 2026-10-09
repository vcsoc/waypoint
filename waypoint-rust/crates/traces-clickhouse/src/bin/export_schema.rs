fn main() {
    println!(
        "{}",
        serde_json::to_string_pretty(&waypoint_traces_clickhouse::wire_schema::schemas()).unwrap()
    );
}
