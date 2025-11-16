import { motion } from "framer-motion";

const TextAnimation = () => {
    return (
        <motion.h1
            style={{ margin:0, fontSize: "300px"}}
            initial = {{color: " #333"}}
            animate = {{ color: ["#f4816d", "#e76e74", "#d06580", "#b85c8a", "#975c9f", "#b85c8a", "#d06580", "#e76e74", "#f4816d"]}}
            transition = {{ duration: 2, repeat: Infinity}}
            >
            Globo
        </motion.h1>
    );
};

export default TextAnimation;