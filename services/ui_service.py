from config import supabase

def get_ui_structure(screen_name: str):
    try:
        screen_res = (
            supabase.table("screen")
            .select("id, name")
            .ilike("name", screen_name)
            .execute()
        )

        if not screen_res.data:
            return {"error": f"'{screen_name}' 화면을 찾을 수 없습니다."}

        screen_id = screen_res.data[0]["id"]

        components = (
            supabase.table("components")
            .select("id, group_name, position_order, region, description")
            .eq("screen_id", screen_id)
            .order("position_order", desc=False)
            .execute()
        ).data

        if not components:
            return {
                "screen": screen_name,
                "components": [],
                "message": f"'{screen_name}' 화면에 등록된 컴포넌트가 없습니다."
            }

        comp_ids = [comp["id"] for comp in components]

        elements = (
            supabase.table("component_elements")
            .select("id, component_id, element_id, element_type, element_label, description")
            .in_("component_id", comp_ids)
            .execute()
        ).data

        component_map = {}
        for comp in components:
            comp_id = comp["id"]
            comp_elements = [
                {
                    "element_id": el["element_id"],
                    "element_type": el["element_type"],
                    "element_label": el["element_label"],
                    "description": el["description"]
                }
                for el in elements if el["component_id"] == comp_id
            ]

            component_map[comp_id] = {
                "group_name": comp["group_name"],
                "position_order": comp["position_order"],
                "region": comp["region"],
                "description": comp["description"],
                "elements": comp_elements
            }

        result = {
            "screen": screen_name,
            "screen_id": screen_id,
            "components": sorted(
                component_map.values(),
                key=lambda c: c["position_order"]
            ),
        }

        return result

    except Exception as e:
        print("❌ [get_ui_structure ERROR]", e)
        return {"error": str(e)}
