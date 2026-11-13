/** @odoo-module **/
import {registry} from "@web/core/registry";
import {Component, onMounted, useRef, useState} from "@odoo/owl";
import {standardFieldProps} from "@web/views/fields/standard_field_props";

export class EQColor extends Component {
    static template = "FieldEQColor";
    static props = {...standardFieldProps};

    setup() {
        this.colorInput = useRef("eq_color_input");
        this.textInput = useRef("eq_text_input");
        this.state = useState({
            color: this.props.record.data[this.props.name] || "#000000",
        });
    }

    get currentColor() {
        return this.props.record.data[this.props.name] || "#000000";
    }

    onColorChange(ev) {
        const newColor = ev.target.value;
        this.state.color = newColor;
        this.props.record.update({[this.props.name]: newColor});
    }

    onTextChange(ev) {
        let newColor = ev.target.value;
        if (newColor && !newColor.startsWith("#")) {
            newColor = "#" + newColor;
        }
        if (/^#[0-9A-Fa-f]{6}$/.test(newColor)) {
            this.state.color = newColor;
            this.props.record.update({[this.props.name]: newColor});
        }
    }
}

registry.category("fields").add("eq_color", {
    component: EQColor,
    supportedTypes: ["char"],
});
